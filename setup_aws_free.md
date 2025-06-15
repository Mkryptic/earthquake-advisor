# 🔐 AWS Setup Guide - Zero/Low Cost Configuration

## 💰 **Cost Overview - What You Need to Know**

### AWS Bedrock Pricing (for Strands Agent)
- **Claude 3 Haiku**: ~$0.25 per 1M input tokens, ~$1.25 per 1M output tokens
- **Claude 3 Sonnet**: ~$3.00 per 1M input tokens, ~$15.00 per 1M output tokens
- **Typical query**: 50-200 tokens = **$0.0001 - $0.001 per question**

### 📊 **Estimated Costs for Demo/Testing**
- **100 test questions**: ~$0.01 - $0.10
- **Demo session (50 questions)**: ~$0.005 - $0.05
- **Full competition demo**: ~$0.10 - $0.50

**Bottom line: Very minimal costs for testing/demo purposes!**

## 🛡️ **Cost Protection Setup**

### 1. Set Up Billing Alerts (CRITICAL)
```bash
# Go to AWS Console > Billing > Billing Preferences
# Enable "Receive Billing Alerts"
# Set alert for $1.00 (will notify before significant costs)
```

### 2. Set Spending Limits
```bash
# AWS Console > Billing > Budgets
# Create budget with $5 limit
# Set alerts at 50%, 80%, 100%
```

### 3. Use the Cheapest Model
We'll configure to use **Claude 3 Haiku** (cheapest option).

## 🔧 **Step-by-Step AWS Setup**

### Step 1: Create AWS Account (Free Tier)
1. Go to [aws.amazon.com](https://aws.amazon.com)
2. Click "Create AWS Account"
3. **Important**: Use the Free Tier (12 months free)
4. Add a credit card (required but won't be charged with proper setup)

### Step 2: Enable Amazon Bedrock
1. AWS Console > Amazon Bedrock
2. Enable model access for:
   - **Anthropic Claude 3 Haiku** (cheapest option)
   - **Anthropic Claude 3 Sonnet** (backup option)

### Step 3: Create IAM User (Security Best Practice)
```bash
# AWS Console > IAM > Users > Create User
# Username: disaster-ready-demo
# Attach policy: AmazonBedrockFullAccess
# Create access key > Command Line Interface (CLI)
```

### Step 4: Get Your Credentials
After creating the IAM user, you'll get:
- **Access Key ID**: AKIA... 
- **Secret Access Key**: wJa...

## 🖥️ **Setting Credentials on Windows**

### Method 1: Environment Variables (Session Only)
```powershell
# In PowerShell (temporary - only for current session)
$env:AWS_ACCESS_KEY_ID="your_access_key_here"
$env:AWS_SECRET_ACCESS_KEY="your_secret_key_here"  
$env:AWS_DEFAULT_REGION="us-east-1"

# Test the credentials
aws sts get-caller-identity
```

### Method 2: Persistent Environment Variables
```powershell
# Set permanent environment variables
[Environment]::SetEnvironmentVariable("AWS_ACCESS_KEY_ID", "your_access_key_here", "User")
[Environment]::SetEnvironmentVariable("AWS_SECRET_ACCESS_KEY", "your_secret_key_here", "User")
[Environment]::SetEnvironmentVariable("AWS_DEFAULT_REGION", "us-east-1", "User")

# Restart PowerShell to use new variables
```

### Method 3: .env File (Recommended for Development)
```bash
# Copy the example file
copy env.example .env

# Edit .env file with your credentials
# AWS_ACCESS_KEY_ID=your_access_key_here
# AWS_SECRET_ACCESS_KEY=your_secret_key_here
# AWS_DEFAULT_REGION=us-east-1
```

### Method 4: AWS CLI Configuration
```powershell
# Install AWS CLI if not installed
# Download from: https://aws.amazon.com/cli/

# Configure credentials
aws configure
# AWS Access Key ID: your_access_key_here
# AWS Secret Access Key: your_secret_key_here  
# Default region: us-east-1
# Default output format: json
```

## ✅ **Testing Your Setup**

### 1. Test AWS Connection
```powershell
# Check if credentials work
aws sts get-caller-identity

# Should return your account info
```

### 2. Test Bedrock Access
```powershell
# List available models
aws bedrock list-foundation-models --region us-east-1

# Should show Claude models
```

### 3. Test the Disaster Ready App
```powershell
# Start the full app with AI agent
python main.py

# Test in another terminal
curl -X POST http://localhost:8000/ask/direct -H "Content-Type: application/json" -d "{\"question\": \"test\"}"
```

## 💡 **Cost Optimization Tips**

### 1. Use Cheapest Model
```python
# We'll configure the app to use Claude 3 Haiku
# Edit agent files if needed to specify model
```

### 2. Limit Token Usage
```python
# Keep questions concise
# Use shorter responses where possible
# Don't run continuous loops
```

### 3. Development vs Demo
```bash
# For development: Use simple_main.py (no AWS costs)
# For demo: Use main.py with AWS (minimal costs)
```

## 🚨 **Emergency Cost Protection**

### If You See Unexpected Charges:
1. **Stop all services immediately**:
   ```powershell
   # Remove AWS credentials
   $env:AWS_ACCESS_KEY_ID=""
   $env:AWS_SECRET_ACCESS_KEY=""
   ```

2. **Check AWS Console**:
   - Billing Dashboard
   - CloudTrail for activity logs
   - Stop any running services

3. **Contact AWS Support**:
   - Free tier includes basic support
   - They're usually helpful with accidental charges

## 🎯 **Recommended Setup for Competition Demo**

### For Minimal Risk:
1. **Set $1 billing alert**
2. **Use environment variables** (session only)
3. **Test with 5-10 questions first**
4. **Use during demo only, remove credentials after**

### Commands to Run:
```powershell
# Set temporary credentials
$env:AWS_ACCESS_KEY_ID="your_key"
$env:AWS_SECRET_ACCESS_KEY="your_secret"
$env:AWS_DEFAULT_REGION="us-east-1"

# Start the app
python main.py

# After demo, clear credentials
$env:AWS_ACCESS_KEY_ID=""
$env:AWS_SECRET_ACCESS_KEY=""
```

## 🆓 **Zero-Cost Alternative**

If you want to avoid AWS entirely:
```powershell
# Use the basic version (no AWS needed)
python simple_main.py

# Still shows:
# ✅ Interactive scenarios
# ✅ Community emergency data  
# ✅ Educational content
# ✅ Basic AI-like responses
# ✅ Professional API
```

## 📞 **Support & Troubleshooting**

### Common Issues:
1. **"No credentials found"**: Check environment variables
2. **"Access denied"**: Verify IAM permissions for Bedrock
3. **"Region not supported"**: Use us-east-1 or us-west-2
4. **"Model not available"**: Enable model access in Bedrock console

### Getting Help:
- AWS Free Tier support is included
- Strands documentation: [strands.ai](https://strands.ai)
- This project includes fallback to basic responses

---

**💰 Expected Demo Cost: $0.05 - $0.50 maximum**  
**⏱️ Setup Time: 15-30 minutes**  
**🛡️ Risk Level: Very Low with proper alerts** 