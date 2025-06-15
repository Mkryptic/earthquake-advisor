# 🚀 Deploy Disaster Ready Simulator to GitHub
# Repository: https://github.com/Mkryptic/earthquake-advisor

Write-Host "🌍 Deploying Disaster Ready: Earthquake Response Simulator" -ForegroundColor Green
Write-Host "📍 Target Repository: https://github.com/Mkryptic/earthquake-advisor" -ForegroundColor Cyan

# Check if git is available
if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Git is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Git: https://git-scm.com/download/win" -ForegroundColor Yellow
    exit 1
}

# Check if we're in the right directory
if (-not (Test-Path "main.py")) {
    Write-Host "❌ Please run this script from the disaster_response_simulator directory" -ForegroundColor Red
    exit 1
}

Write-Host "`n🔧 Setting up Git repository..." -ForegroundColor Yellow

# Initialize git if not already done
if (-not (Test-Path ".git")) {
    git init
    Write-Host "✅ Git repository initialized" -ForegroundColor Green
} else {
    Write-Host "✅ Git repository already exists" -ForegroundColor Green
}

# Add remote origin
Write-Host "`n🔗 Adding remote repository..." -ForegroundColor Yellow
git remote remove origin 2>$null  # Remove if exists
git remote add origin https://github.com/Mkryptic/earthquake-advisor.git
Write-Host "✅ Remote origin set to earthquake-advisor" -ForegroundColor Green

# Create .gitignore if it doesn't exist
if (-not (Test-Path ".gitignore")) {
    Write-Host "`n📝 Creating .gitignore..." -ForegroundColor Yellow
    @"
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
share/python-wheels/
*.egg-info/
.installed.cfg
*.egg
MANIFEST

# Environment variables
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# AWS credentials
.aws/
aws-credentials.txt
*.pem

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Logs
*.log
logs/

# Temporary files
*.tmp
*.temp
"@ | Out-File -FilePath ".gitignore" -Encoding UTF8
    Write-Host "✅ .gitignore created" -ForegroundColor Green
} else {
    Write-Host "✅ .gitignore already exists" -ForegroundColor Green
}

# Stage all files
Write-Host "`n📦 Staging files for commit..." -ForegroundColor Yellow
git add .
Write-Host "✅ Files staged" -ForegroundColor Green

# Check if there are changes to commit
$status = git status --porcelain
if ($status) {
    # Commit changes
    Write-Host "`n💾 Committing changes..." -ForegroundColor Yellow
    $commitMessage = "🚀 Initial deployment: Disaster Ready Earthquake Response Simulator

Features:
- 🤖 AI-powered emergency advisor using AWS Bedrock
- 📚 Interactive earthquake scenarios with scoring
- 🏥 Southeast Asia emergency resources (Thailand/Myanmar)
- 🌐 Multi-language support (English, Thai, Burmese)
- 👥 Multi-agent emergency response coordination
- 🐳 Docker deployment ready
- 💰 Cost-optimized AWS integration

Demo ready with both zero-cost basic version and full AI capabilities!"

    git commit -m $commitMessage
    Write-Host "✅ Changes committed" -ForegroundColor Green
} else {
    Write-Host "ℹ️ No changes to commit" -ForegroundColor Blue
}

# Push to GitHub
Write-Host "`n🚀 Pushing to GitHub..." -ForegroundColor Yellow
try {
    git branch -M main
    git push -u origin main --force
    Write-Host "✅ Successfully deployed to GitHub!" -ForegroundColor Green
    Write-Host "`n🎉 Deployment Complete!" -ForegroundColor Magenta
    Write-Host "🔗 Repository: https://github.com/Mkryptic/earthquake-advisor" -ForegroundColor Cyan
    Write-Host "📚 View README: https://github.com/Mkryptic/earthquake-advisor#readme" -ForegroundColor Cyan
} catch {
    Write-Host "❌ Failed to push to GitHub" -ForegroundColor Red
    Write-Host "This might be due to authentication issues." -ForegroundColor Yellow
    Write-Host "`nPlease set up Git authentication:" -ForegroundColor Yellow
    Write-Host "1. Personal Access Token: https://github.com/settings/tokens" -ForegroundColor White
    Write-Host "2. Or use GitHub CLI: gh auth login" -ForegroundColor White
    Write-Host "`nThen run: git push -u origin main" -ForegroundColor White
}

Write-Host "`n🎯 Next Steps:" -ForegroundColor Yellow
Write-Host "1. ✅ Code deployed to GitHub" -ForegroundColor Green
Write-Host "2. 🔧 Set up GitHub Actions (optional)" -ForegroundColor White
Write-Host "3. 🌐 Enable GitHub Pages for documentation" -ForegroundColor White
Write-Host "4. 📱 Test the deployed version" -ForegroundColor White
Write-Host "5. 🏆 Ready for demo/competition!" -ForegroundColor Green

Write-Host "`n📖 Quick Test Commands:" -ForegroundColor Yellow
Write-Host "git clone https://github.com/Mkryptic/earthquake-advisor.git" -ForegroundColor White
Write-Host "cd earthquake-advisor" -ForegroundColor White
Write-Host "python simple_main.py  # Test basic version" -ForegroundColor White
Write-Host "python main.py         # Test AI version (AWS required)" -ForegroundColor White

Write-Host "`n🌍 Your Disaster Ready Simulator is now live on GitHub! 🚀" -ForegroundColor Green 