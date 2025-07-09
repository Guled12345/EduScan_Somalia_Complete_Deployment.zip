# Installation Guide - EduScan Somalia

## Quick Start

### 1. Download and Extract
Download the complete deployment package and extract all files to a folder.

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Application
```bash
streamlit run app.py
```

## Render Deployment Steps

### 1. Create GitHub Repository
- Create a new repository on GitHub
- Upload all files from this package
- Ensure all files are in the root directory

### 2. Connect to Render
- Go to https://render.com
- Create new account or sign in
- Click "New" → "Web Service"
- Connect your GitHub repository

### 3. Configure Deployment
- Build Command: `pip install -r requirements.txt`
- Start Command: `streamlit run app.py --server.port $PORT --server.address 0.0.0.0 --server.headless true`
- Python Version: 3.11.9

### 4. Deploy
- Click "Deploy Web Service"
- Wait for deployment to complete
- Access your application at the provided URL

## File Requirements
Make sure these files are present:
- ✅ app.py
- ✅ pages/ folder with all page files
- ✅ utils/ folder with all utility files
- ✅ data/ folder with ML model files
- ✅ .streamlit/ folder with config
- ✅ requirements.txt
- ✅ runtime.txt
- ✅ render.yaml
- ✅ Procfile

## Troubleshooting
- If deployment fails, check Python version compatibility
- Ensure all dependencies are in requirements.txt
- Verify ML model files are in data/ folder
- Check Streamlit configuration in .streamlit/config.toml