# GitHub Setup Guide for Grid Escape Game

Follow these steps to set up automatic building of executables for Windows, macOS, and Linux.

## Step 1: Create a GitHub Account

1. Go to [github.com](https://github.com)
2. Click "Sign up" and create a free account
3. Verify your email address

## Step 2: Create a New Repository

1. Click the "+" icon in the top right corner
2. Select "New repository"
3. Fill in the details:
   - **Repository name**: `grid-escape-game`
   - **Description**: `A strategic two-player grid-based escape game`
   - **Visibility**: Public (required for free GitHub Actions)
   - **Initialize**: Don't check any boxes (we'll upload our files)
4. Click "Create repository"

## Step 3: Upload Your Game Files

### Option A: Using GitHub Web Interface (Easier)

1. On your new repository page, click "uploading an existing file"
2. Drag and drop ALL your game files and folders:
   - `pygame_grid_escape/` folder (entire folder)
   - `.github/` folder (entire folder)
   - `README.md`
   - `requirements.txt`
   - `LICENSE`
   - `.gitignore`
   - All other files I created
3. Write a commit message: "Initial game upload"
4. Click "Commit changes"

### Option B: Using Git Command Line (Advanced)

```bash
# Clone your repository
git clone https://github.com/YOUR_USERNAME/grid-escape-game.git
cd grid-escape-game

# Copy all your game files to this directory
# Then add and commit them
git add .
git commit -m "Initial game upload"
git push origin main
```

## Step 4: Trigger the Build

1. Go to your repository on GitHub
2. Click the "Actions" tab
3. You should see "Build Grid Escape Executables" workflow
4. If it doesn't start automatically, click "Run workflow"

## Step 5: Download Your Executables

1. Wait for the build to complete (usually 5-10 minutes)
2. Click on the completed workflow run
3. Scroll down to "Artifacts"
4. Download:
   - `GridEscape-Windows` (contains the .exe file)
   - `GridEscape-macOS` (contains the macOS executable)
   - `GridEscape-Linux` (contains the Linux executable)

## Step 6: Create a Release (Optional but Recommended)

1. Go to your repository main page
2. Click "Releases" on the right side
3. Click "Create a new release"
4. Tag version: `v1.0.0`
5. Release title: `Grid Escape Game v1.0.0`
6. Upload the executable files you downloaded
7. Write release notes describing your game
8. Click "Publish release"

## Step 7: Share Your Game

Now you can share your game by:
1. **Direct download**: Send people the link to your release page
2. **Individual files**: Share the specific executable files
3. **Repository link**: Share your repository URL

## Automatic Updates

Every time you:
1. Make changes to your game code
2. Push the changes to GitHub
3. The executables will be automatically rebuilt!

## Example Repository Structure

Your repository should look like this:
```
grid-escape-game/
├── .github/
│   └── workflows/
│       └── build-executables.yml
├── pygame_grid_escape/
│   ├── game_logic/
│   ├── input/
│   ├── rendering/
│   └── main.py
├── README.md
├── requirements.txt
├── LICENSE
└── .gitignore
```

## Troubleshooting

### Build Fails
- Check the Actions tab for error messages
- Make sure all Python files are valid
- Ensure pygame_grid_escape/main.py exists

### Can't Download Executables
- Make sure the build completed successfully
- Artifacts are only available for 90 days
- Create a release for permanent downloads

### Executables Don't Work
- Test on a clean machine without Python
- Check antivirus isn't blocking the files
- Try building without `--onefile` flag if needed

## Need Help?

If you run into issues:
1. Check the Actions tab for build logs
2. Look at the error messages
3. Make sure all files are uploaded correctly
4. Ensure the pygame_grid_escape folder structure is correct