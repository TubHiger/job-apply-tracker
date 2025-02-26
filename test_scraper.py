import requests
from bs4 import BeautifulSoup

job_url = "https://www.pinterestcareers.com/jobs/6483208/senior-business-intelligence-analyst/?gh_jid=6483208"
headers = {"User-Agent": "Mozilla/5.0"}

response = requests.get(job_url, headers=headers)

if response.status_code == 200:
    soup = BeautifulSoup(response.text, "html.parser")
    
    # Extract job details
    job_title = soup.find("h1")
    company_name = soup.find("meta", {"property": "og:site_name"})
    location = soup.find("span", class_="location")

    print("Job Title:", job_title.text.strip() if job_title else "Not Found")
    print("Company Name:", company_name["content"].strip() if company_name else "Not Found")
    print("Location:", location.text.strip() if location else "Not Found")
else:
    print(f"❌ Failed to load page. Status Code: {response.status_code}")
