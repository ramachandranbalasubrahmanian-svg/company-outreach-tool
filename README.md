# LinkedIn Company Outreach Automation

This tool automates the process of finding professionals (Recruiters, Product Leaders, Senior Leadership) at specific companies using the LinkedIn API. It extracts their details and generates best-guess email addresses.

## Features
- **Authenticated Search**: Uses your LinkedIn credentials to fetch real profiles.
- **Role Filtering**: Automatically categorizes profiles into:
  - HR/Recruiting
  - Product Leadership
  - Senior Leadership (VP/Director)
- **Email Guessing**: Generates potential email addresses based on name and company domain.
- **Configurable**: Run for specific companies, locations, and profile counts.
- **Export**: Saves results to a CSV file.

## Prerequisites
- Python 3.x
- A LinkedIn account

## Installation

1.  **Clone the repository**:
    ```bash
    git clone <repository_url>
    cd company_outreach_public
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Setup Credentials**:
    - Rename `credentials.example.json` to `credentials.json`.
    - Open `credentials.json` and enter your LinkedIn email and password.
    ```json
    {
        "username": "your_email@example.com",
        "password": "your_password"
    }
    ```
    > **Note**: Your credentials are stored locally and added to `.gitignore`. They are NOT shared.

## Usage

Run the script from the terminal:

```bash
python3 main.py --companies "Company1, Company2" --location "Location" --count 10
```

### Arguments
- `--companies`: Comma-separated list of companies (max 5).
- `--location`: Target location (e.g., "Bangalore", "San Francisco", "Worldwide").
- `--count`: Number of profiles to fetch per company (max 20).

### Example

```bash
python3 main.py --companies "Google, Microsoft" --location "Bangalore" --count 5
```

## Output
The script generates a CSV file for each company with the format:
`CompanyName_Date_Contact.csv`

**Example Output (`Google_27-11-2025_Contact.csv`):**
```csv
Company,Name,Title (Inferred),Email (Guessed),Profile URL,Group
Google,John Doe,Recruiter,john.doe@google.com,https://www.linkedin.com/in/...,HR/Recruiting
```

## Disclaimer
This tool is for educational purposes. Automating LinkedIn actions may violate their Terms of Service. Use responsibly and avoid excessive requests to prevent account restriction.
