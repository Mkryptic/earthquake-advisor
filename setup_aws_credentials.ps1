# 🔐 AWS Credentials Setup Script for Disaster Ready Simulator
# Run this script to set up AWS credentials safely

Write-Host "🌍 Disaster Ready: AWS Credentials Setup" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green

# Check if AWS CLI is installed
try {
    aws --version | Out-Null
    Write-Host "✅ AWS CLI found" -ForegroundColor Green
} catch {
    Write-Host "⚠️  AWS CLI not found. You can still set environment variables manually." -ForegroundColor Yellow
}

Write-Host ""
Write-Host "💰 COST INFORMATION:" -ForegroundColor Cyan
Write-Host "   • Typical demo cost: $0.05 - $0.50" -ForegroundColor White
Write-Host "   • Cost per question: ~$0.0001 - $0.001" -ForegroundColor White
Write-Host "   • Recommended: Set $1 billing alert first" -ForegroundColor White

Write-Host ""
Write-Host "🔧 Setting up credentials for this session only..." -ForegroundColor Yellow

# Get credentials from user
$AccessKey = Read-Host "Enter your AWS Access Key ID"
$SecretKey = Read-Host "Enter your AWS Secret Access Key" -AsSecureString
$SecretKeyPlain = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($SecretKey))
$Region = Read-Host "Enter AWS Region (press Enter for us-east-1)"

if ([string]::IsNullOrWhiteSpace($Region)) {
    $Region = "us-east-1"
}

# Set environment variables for this session
$env:AWS_ACCESS_KEY_ID = $AccessKey
$env:AWS_SECRET_ACCESS_KEY = $SecretKeyPlain
$env:AWS_DEFAULT_REGION = $Region

Write-Host ""
Write-Host "✅ Credentials set for this PowerShell session!" -ForegroundColor Green

# Test credentials if AWS CLI is available
try {
    Write-Host "🔍 Testing credentials..." -ForegroundColor Yellow
    $identity = aws sts get-caller-identity 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✅ AWS credentials working!" -ForegroundColor Green
        Write-Host $identity
        
        # Test Bedrock access
        Write-Host "🧠 Testing Bedrock access..." -ForegroundColor Yellow
        $models = aws bedrock list-foundation-models --region $Region 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✅ Bedrock access confirmed!" -ForegroundColor Green
        } else {
            Write-Host "⚠️  Bedrock access issue. Check permissions." -ForegroundColor Yellow
        }
    } else {
        Write-Host "❌ Credentials test failed. Please check your keys." -ForegroundColor Red
    }
} catch {
    Write-Host "⚠️  Could not test credentials (AWS CLI issue)" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "🚀 Ready to start! Choose one:" -ForegroundColor Cyan
Write-Host "   Full AI: python main.py" -ForegroundColor White
Write-Host "   Basic:   python simple_main.py" -ForegroundColor White

Write-Host ""
Write-Host "🛡️  SECURITY REMINDER:" -ForegroundColor Red
Write-Host "   • These credentials are only set for this session" -ForegroundColor White
Write-Host "   • Close PowerShell to clear them" -ForegroundColor White
Write-Host "   • Monitor AWS billing dashboard" -ForegroundColor White

Write-Host ""
Write-Host "🧹 To clear credentials manually:" -ForegroundColor Yellow
Write-Host '   $env:AWS_ACCESS_KEY_ID=""' -ForegroundColor Gray
Write-Host '   $env:AWS_SECRET_ACCESS_KEY=""' -ForegroundColor Gray 