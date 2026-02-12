# Google Earth Engine Setup Guide
## Get Authenticated in 3 Steps

### Step 1: Sign Up for Earth Engine Access
**URL**: https://code.earthengine.google.com/

Actions:
1. Click "Get Started" or sign in with your Google account
2. You'll be prompted to register for Earth Engine
3. Select or create a Google Cloud Project
   - If you don't have one, it will guide you through creation
   - Free tier is sufficient for this pipeline

### Step 2: Register a Cloud Project (if needed)
**URL**: https://console.cloud.google.com/projectcreate

Actions:
1. Create a new project (or select existing)
2. Project name: "soweto-climate-analysis" (or your choice)
3. Click "Create"
4. **Copy the Project ID** - you'll need this

### Step 3: Enable Earth Engine API for Your Project
**URL**: https://console.cloud.google.com/apis/library/earthengine.googleapis.com

Actions:
1. Make sure your project is selected (top navbar)
2. Click "Enable" button
3. Wait for API to enable (~30 seconds)

### Step 4: Authenticate from CLI
Run this command in your terminal:

```bash
earthengine authenticate
```

This will:
1. Open a browser window
2. Ask you to select your Google account
3. Request permission to access Earth Engine
4. Generate a verification code
5. Paste the code back in terminal

### Alternative: Service Account (for sharing/automation)
**URL**: https://console.cloud.google.com/iam-admin/serviceaccounts

If you need to share credentials or run automated pipelines:
1. Create Service Account
2. Grant "Earth Engine Resource Writer" role
3. Create JSON key
4. Download credentials file
5. Set environment variable:
   ```bash
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/credentials.json"
   ```

---

## Quick Links

| Purpose | URL |
|---------|-----|
| Earth Engine Sign Up | https://code.earthengine.google.com/ |
| Create Cloud Project | https://console.cloud.google.com/projectcreate |
| Enable EE API | https://console.cloud.google.com/apis/library/earthengine.googleapis.com |
| Service Accounts | https://console.cloud.google.com/iam-admin/serviceaccounts |
| Manage Projects | https://console.cloud.google.com/cloud-resource-manager |
| EE Asset Manager | https://code.earthengine.google.com/assets |

---

## Verification Commands

After authentication, test with:

```bash
# Test CLI access
earthengine ls

# Test Python API
python3 test_gee_connection.py

# Check authenticated account
earthengine authenticate --status
```

---

## Troubleshooting

**"Not signed up for Earth Engine"**
→ Complete Step 1 above

**"Project is not registered"**
→ Complete Steps 2-3 above

**"Permission denied"**
→ Make sure Earth Engine API is enabled (Step 3)
→ Wait a few minutes after enabling API

**Need to share access with collaborators**
→ Use Service Account method (see Alternative section)
→ Share the JSON key file securely
