import gspread
from google.oauth2.service_account import Credentials
import functions_framework
import requests
from bs4 import BeautifulSoup
import os
from google.cloud import storage
from datetime import datetime

# 📌 CONFIGURATION
BUCKET_NAME = "your-backet-name"  # Change to your Cloud Storage bucket
JSON_FILE_NAME = "your-service-account.json"
SERVICE_ACCOUNT_FILE = f"/tmp/{JSON_FILE_NAME}"

# ✅ Download service account JSON from Cloud Storage
def download_service_account_json():
    storage_client = storage.Client()
    bucket = storage_client.bucket(BUCKET_NAME)
    blob = bucket.blob(JSON_FILE_NAME)
    blob.download_to_filename(SERVICE_ACCOUNT_FILE)

# 🛠 Ensure JSON file is available before authentication
download_service_account_json()

# 🔐 Authenticate with Google Sheets
SCOPES = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(creds)

# 📊 Google Sheet Setup
SHEET_ID = "your-google-sheet-id"  # Replace with your actual sheet ID
spreadsheet = client.open_by_key(SHEET_ID)
job_links_sheet = spreadsheet.worksheet("job_links")
job_details_sheet = spreadsheet.worksheet("job_details")

# 🔍 Function to Scrape Job Details
def scrape_job_details(job_url):
    """Scrapes job details from a given job posting URL."""
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(job_url, headers=headers)

    if response.status_code != 200:
        print(f"❌ Failed to fetch job page: {job_url} (Status: {response.status_code})")
        return None

    soup = BeautifulSoup(response.text, "html.parser")

    job_title = soup.find("h1")
    company_name = soup.find("meta", {"property": "og:site_name"})
    location = soup.find("span", class_="location")

    job_data = {
        "date_applied": datetime.today().strftime('%B %d, %Y'),  # Format: January 1, 2025
        "company_name": company_name["content"].strip() if company_name else "Unknown",
        "position_name": job_title.text.strip() if job_title else "Unknown",
        "location": location.text.strip() if location else "Unknown",
        "job_link": job_url
    }

    print("✅ Scraped Job Data:", job_data)  # Debugging output

    return job_data

# 🚀 Cloud Function to Update Google Sheet
@functions_framework.http
def update_google_sheet(request):
    """Reads job links from Google Sheets, scrapes job details, and updates another tab without duplicates."""
    
    # Read job links from job_links tab
    job_links = job_links_sheet.col_values(1)[1:]  # Skip header
    print("🔍 Job Links Read from Sheet:", job_links)

    # Read existing job links from job_details tab
    existing_links = job_details_sheet.col_values(5)[1:]  # Skip header, column 5 = job link
    print("📌 Existing Job Links in Sheet:", existing_links)

    for job_url in job_links:
        if job_url in existing_links:
            print(f"⚠️ Skipping duplicate: {job_url}")
            continue  # Skip if already in job_details

        job_data = scrape_job_details(job_url)
        if job_data:
            job_details_sheet.append_row([
                job_data["date_applied"],
                job_data["company_name"],
                job_data["position_name"],
                job_data["location"],
                job_data["job_link"]
            ])
            print(f"✅ Added new job entry: {job_url}")

    return "✅ Job details updated without duplicates!", 200
