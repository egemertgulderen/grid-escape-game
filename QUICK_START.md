# 🚀 Quick Start Guide - Get Your Executables in 10 Minutes!

Follow these simple steps to get Windows, macOS, and Linux executables of your Grid Escape game.

## ⏱️ 10-Minute Setup

### Step 1: Create GitHub Account (2 minutes)
1. Go to [github.com](https://github.com)
2. Click "Sign up" 
3. Create your account and verify email

### Step 2: Create Repository (2 minutes)
1. Click the "+" icon → "New repository"
2. Name: `grid-escape-game`
3. Description: `Strategic two-player grid escape game`
4. Make it **Public** (required for free builds)
5. Click "Create repository"

### Step 3: Upload Files (3 minutes)
1. Click "uploading an existing file" on your new repo
2. **Drag and drop ALL these folders and files:**
   ```
   📁 pygame_grid_escape/     (entire folder)
   📁 .github/               (entire folder)
   📄 README.md
   📄 requirements.txt
   📄 LICENSE
   📄 .gitignore
   📄 GITHUB_SETUP_GUIDE.md
   📄 (all other .md files)
   ```
3. Commit message: "Initial upload"
4. Click "Commit changes"

### Step 4: Wait for Build (3 minutes)
1. Go to "Actions" tab in your repository
2. Watch the build process (takes 2-5 minutes)
3. ✅ Green checkmark = Success!

### Step 5: Download Executables (1 minute)
1. Click on the completed build
2. Scroll to "Artifacts" section
3. Download:
   - `GridEscape-Windows` → Contains `.exe` file
   - `GridEscape-macOS` → Contains macOS app
   - `GridEscape-Linux` → Contains Linux executable

## 🎉 You're Done!

You now have:
- ✅ **GridEscape-Windows.exe** - For Windows users
- ✅ **GridEscape-macOS** - For Mac users  
- ✅ **GridEscape-Linux** - For Linux users

## 📤 Sharing Your Game

### Option 1: Direct File Sharing
Send the executable files directly to your friends!

### Option 2: Create a Release (Recommended)
1. Go to your repo → "Releases" → "Create new release"
2. Tag: `v1.0.0`
3. Title: `Grid Escape Game v1.0.0`
4. Upload your executable files
5. Click "Publish release"
6. Share the release URL!

## 🔄 Automatic Updates

Every time you make changes:
1. Upload new files to GitHub
2. Executables rebuild automatically
3. Download the latest versions

## ❓ Need Help?

- **Build failed?** Check the "Actions" tab for error messages
- **Files missing?** Run `python3 prepare_for_github.py` to check
- **Can't upload?** Make sure you're uploading ALL folders and files

## 🎮 Test Your Executables

Before sharing:
1. Download each executable
2. Test on different computers
3. Make sure they run without Python installed

---

**That's it! Your game is now ready for the world! 🌟**