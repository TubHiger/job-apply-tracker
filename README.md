# Job Application Tracker

This project automates job tracking using Google Cloud Functions and Google Sheets.

## 🚀 Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/job-apply-tracker.git
2. Install dependencies:
   ```bash 
   pip install -r requirements.txt
3. Set up environment variables:
   ```bash 
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your-service-account.json"
   export GOOGLE_SHEET_ID="your-google-sheet-id"
4. Deploy the function:
   ```bash 
   gcloud functions deploy update_google_sheet \
    --runtime python310 \
    --trigger-http \
    --allow-unauthenticated \
    --entry-point update_google_sheet \
    --source=. \
    --no-gen2

---

