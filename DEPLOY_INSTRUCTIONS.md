# Deploy to Streamlit Cloud - Step by Step

## 1. Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `landing-page-generator`
3. Description: "High-converting landing page generator"
4. Set to **Public** (or Private if you have GitHub Pro)
5. DON'T initialize with README (we already have one)
6. Click "Create repository"

## 2. Push Code to GitHub

Open Windows PowerShell or Git Bash and run these commands:

```bash
cd C:\Users\Niklas\PycharmProjects\Crawler\LandingPageGenerator

# Initialize git
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit - Landing Page Generator"

# Add your GitHub repository (replace YOUR_USERNAME)
git remote add origin https://github.com/YOUR_USERNAME/landing-page-generator.git

# Push to GitHub
git push -u origin main
```

If it says "main" doesn't exist, try:
```bash
git push -u origin master
```

## 3. Deploy on Streamlit

1. Go to https://share.streamlit.io/
2. Click "New app"
3. Connect your GitHub account if needed
4. Select:
   - Repository: `YOUR_USERNAME/landing-page-generator`
   - Branch: `main` (or `master`)
   - Main file path: `app.py`
5. Click "Deploy"

## 4. Your App is Live!

- Your app will be at: `https://YOUR_APP_NAME.streamlit.app`
- Users MUST enter their own API key when they visit
- Your API key is NOT included or exposed
- Share the link with your team!

## Security Check ✅

- No API keys in code ✓
- Users enter their own keys ✓
- Keys only last for session ✓
- .gitignore excludes sensitive files ✓