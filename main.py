import sys
import os
import csv
import argparse
from datetime import datetime
from linkedin_searcher import search_people, extract_name_from_url
from email_finder import generate_emails

def main():
    parser = argparse.ArgumentParser(description="Search for professionals at specific companies.")
    parser.add_argument("--companies", required=True, help="Comma-separated list of companies (max 5)")
    parser.add_argument("--location", required=True, help="Location to search in (e.g., 'Bangalore', 'London')")
    parser.add_argument("--count", type=int, default=10, help="Total number of people to fetch per company (max 20)")
    
    args = parser.parse_args()
    
    # Parse companies
    target_companies = [c.strip() for c in args.companies.split(",") if c.strip()]
    location = args.location
    total_count = args.count
    
    if len(target_companies) > 5:
        print("Error: You can provide a maximum of 5 companies.")
        return
        
    if not target_companies:
        print("Error: No companies provided.")
        return

    if total_count > 20:
        print("Error: Count cannot exceed 20.")
        return
        
    # Distribute count across 3 groups (approx 30%, 30%, 40%)
    c1 = int(total_count * 0.3)
    c2 = int(total_count * 0.3)
    c3 = total_count - c1 - c2
    
    # Ensure at least 1 per group if total_count >= 3
    if total_count >= 3:
        c1 = max(1, c1)
        c2 = max(1, c2)
        c3 = total_count - c1 - c2

    print(f"Starting AUTHENTICATED search for {len(target_companies)} companies in {location} (Target: {total_count} profiles/company)...")

    # Define the groups
    group1_roles = ["Recruiter", "Talent Acquisition", "HR", "Human Resources"]
    group2_roles = ["Product Leader", "Product Lead", "Group Product Manager", "Head of Product"]
    group3_roles = ["VP", "Vice President", "Senior Director", "Director"]

    for company in target_companies: 
        print(f"Processing {company}...")
        
        company_targets = []
        
        # Group 1
        if c1 > 0:
            targets1 = search_people(company, group1_roles, location, count=c1)
            for t in targets1:
                t['group'] = "HR/Recruiting"
                company_targets.append(t)
            
        # Group 2
        if c2 > 0:
            targets2 = search_people(company, group2_roles, location, count=c2)
            for t in targets2:
                t['group'] = "Product Leadership"
                company_targets.append(t)
            
        # Group 3
        if c3 > 0:
            targets3 = search_people(company, group3_roles, location, count=c3)
            for t in targets3:
                t['group'] = "Senior Leadership"
                company_targets.append(t)

        # Generate filename: Company_name_date(dd-mm-yyyy)_Contact.csv
        date_str = datetime.now().strftime("%d-%m-%Y")
        safe_company_name = company.replace(" ", "_").replace("/", "_")
        output_file = f"{safe_company_name}_{date_str}_Contact.csv"

        # Process data and write to CSV
        with open(output_file, "w", newline="") as csvfile:
            fieldnames = ["Company", "Name", "Title (Inferred)", "Email (Guessed)", "Profile URL", "Group"]
            
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for target in company_targets:
                name = target.get('name')
                if not name:
                    name = extract_name_from_url(target['profile_url'])
                
                email = generate_emails(name, target['company'])
                
                writer.writerow({
                    "Company": target['company'],
                    "Name": name,
                    "Title (Inferred)": target['title_snippet'],
                    "Email (Guessed)": email,
                    "Profile URL": target['profile_url'],
                    "Group": target['group']
                })
                
        print(f"Done! Saved {len(company_targets)} profiles to {output_file}")

if __name__ == "__main__":
    main()
