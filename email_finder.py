def generate_emails(name, company):
    """
    Generates potential email addresses for a person at a company.
    """
    if not name or name == "Unknown":
        return ""
    
    # Remove parentheses and content within them (e.g. pronouns)
    import re
    name = re.sub(r'\([^)]*\)', '', name).strip()
    
    parts = name.lower().split()
    if len(parts) < 2:
        return ""
    
    # Remove non-alphabetic characters from parts
    parts = ["".join(filter(str.isalpha, p)) for p in parts]
    parts = [p for p in parts if p] # Remove empty strings
    
    if len(parts) < 2:
        return ""
        
    first = parts[0]
    last = parts[-1]
    
    # Clean company name (remove Inc, Pvt Ltd, etc)
    company_domain = company.lower().replace(" ", "").replace(".", "").replace(",", "")
    # Heuristic: most tech companies use company.com. 
    # Real implementation would need a domain lookup.
    domain = f"{company_domain}.com"
    
    # Common patterns
    emails = [
        f"{first}.{last}@{domain}",
        f"{first}{last}@{domain}",
        f"{first}@{domain}",
        f"{first}_{last}@{domain}"
    ]
    
    # Return the most likely one (first.last is very common) 
    # or all of them joined. The user asked for "actual mail id", 
    # so we will provide the most standard format.
    return emails[0]
