from linkedin_api import Linkedin
import json
import time
import random
import os

# Global client instance
api = None

def init_api():
    global api
    creds_file = "credentials.json"
    if not os.path.exists(creds_file):
        raise FileNotFoundError("credentials.json not found. Please create it with 'username' and 'password' keys.")
    
    with open(creds_file, "r") as f:
        creds = json.load(f)
        
    username = creds.get("username")
    password = creds.get("password")
    
    if not username or not password:
        raise ValueError("credentials.json must contain 'username' and 'password'.")
        
    print(f"Authenticating as {username}...")
    api = Linkedin(username, password)
    print("Authentication successful!")

def get_company_urn(company_name):
    """
    Searches for the company and returns its URN ID.
    """
    global api
    if api is None:
        init_api()
        
    try:
        results = api.search_companies(keywords=company_name, limit=1)
        if results:
            return results[0]['urn_id']
    except Exception as e:
        print(f"Error fetching company URN for {company_name}: {e}")
    return None

def search_people(company, role_keywords, location, count=3):
    """
    Searches for profiles using the authenticated LinkedIn API.
    Ensures the person is CURRENTLY working at the company.
    """
    global api
    if api is None:
        init_api()
        
    print(f"Searching LinkedIn for {company} - {role_keywords} in {location}...")
    
    results = []
    try:
        # 1. Get Company URN
        company_urn = get_company_urn(company)
        if not company_urn:
            print(f"Could not find company URN for {company}. Skipping.")
            return []
            
        print(f"Found URN for {company}: {company_urn}")
        
        # 2. Search People with current_company filter
        # We join keywords for role, but keep company strict via URN
        keywords = f"{' '.join(role_keywords)}"
        if location:
            keywords += f" {location}"
        
        search_hits = api.search_people(
            keywords=keywords, 
            current_company=[company_urn],
            limit=count*2
        )
        
        if search_hits:
            print(f"DEBUG: First hit structure: {search_hits[0]}")
        
        for hit in search_hits:
            if len(results) >= count:
                break
            
            urn_id = hit.get('urn_id')
            name = hit.get('name', 'Unknown')
            jobtitle = hit.get('jobtitle', '')
            location_name = hit.get('location', '')
            
            # Validation for "Regular User"
            # 1. Name should not be "LinkedIn Member" (common for out-of-network)
            # 2. Name should not be "Unknown"
            # 3. Job Title should not be empty
            if name in ["LinkedIn Member", "Unknown"] or not jobtitle:
                continue
            
            profile_url = f"https://www.linkedin.com/in/{urn_id}"
            
            results.append({
                "company": company,
                "role_type": "/".join(role_keywords[:2]),
                "profile_url": profile_url,
                "title_snippet": f"{jobtitle} | {location_name}",
                "name": name
            })
            
            # Random sleep
            time.sleep(random.uniform(2, 5))
            
    except Exception as e:
        print(f"Error searching for {company}: {e}")
        
    return results

def extract_name_from_url(url):
    # We might already have the name from the API object, but to keep interface consistent:
    try:
        slug = url.split("/in/")[-1].split("/")[0]
        parts = slug.split("-")
        clean_parts = [p for p in parts if not p.isdigit()]
        name = " ".join(clean_parts).title()
        return name
    except:
        return "Unknown"
