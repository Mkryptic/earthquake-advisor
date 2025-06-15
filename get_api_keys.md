# 🔑 Getting API Access Keys for Disaster Ready Simulator

## 📋 **You Have Console Access - Now Get API Keys**

Your console credentials:
- **Console URL**: https://061348119888.signin.aws.amazon.com/console
- **Username**: disaster-ready-demo
- **Password**: ietUF|7)

**Next step**: Get programmatic access keys for the Python application.

## 🔧 **Step-by-Step: Get API Keys**

### 1. Log into AWS Console
1. Go to: https://061348119888.signin.aws.amazon.com/console
2. Username: `disaster-ready-demo`
3. Password: `ietUF|7)`

### 2. Navigate to IAM
1. In the AWS Console, search for "IAM"
2. Click on "IAM" service

### 3. Go to Your User
1. Click "Users" in the left sidebar
2. Click on "disaster-ready-demo" (your username)

### 4. Create Access Keys
1. Click the "Security credentials" tab
2. Scroll down to "Access keys" section
3. Click "Create access key"
4. Select "Command Line Interface (CLI)"
5. Check the confirmation box
6. Click "Next"
7. Add description: "Disaster Ready Simulator"
8. Click "Create access key"

### 5. IMPORTANT: Save Your Keys
You'll see:
- **Access key ID**: AKIA... (starts with AKIA)
- **Secret access key**: (long random string)

**⚠️ CRITICAL**: Copy both keys immediately - you won't see the secret again!

## 🛡️ **Security Reminders**

### Before Creating Keys:
1. **Set Billing Alert**: 
   - AWS Console > Billing > Budgets
   - Create $1 budget alert

2. **Verify Bedrock Access**:
   - AWS Console > Amazon Bedrock
   - Model access > Enable Anthropic Claude models

### After Getting Keys:
- **Don't share them publicly** (like in chat/email)
- **Use them only for this project**
- **Delete them after your demo/competition**

## 🚀 **Using Your Keys**

Once you have your access keys, you can use them with our setup script:

```powershell
# Run the setup script
.\setup_aws_credentials.ps1

# When prompted, enter:
# Access Key ID: AKIA... (your key)
# Secret Access Key: (your secret)
# Region: us-east-1
```

Or set them manually:
```powershell
$env:AWS_ACCESS_KEY_ID="AKIA..." 
$env:AWS_SECRET_ACCESS_KEY="your_secret_key"
$env:AWS_DEFAULT_REGION="us-east-1"

# Test the full AI version
python main.py
```

## ✅ **Testing Checklist**

After setting up keys:
1. **Test AWS connection**: `aws sts get-caller-identity`
2. **Test Bedrock**: `aws bedrock list-foundation-models --region us-east-1`
3. **Start the app**: `python main.py`
4. **Test endpoint**: Visit http://localhost:8000/docs

## 🔍 **Troubleshooting**

### Common Issues:
- **"Access Denied"**: Need to enable Bedrock model access
- **"No credentials"**: Environment variables not set
- **"Region not supported"**: Use us-east-1 or us-west-2

### If Something Goes Wrong:
1. **Double-check**: Bedrock model access enabled
2. **Verify**: Keys copied correctly (no extra spaces)
3. **Try**: Different region (us-west-2)
4. **Fallback**: Use `python simple_main.py` (zero cost)

---

**💰 Remember**: Demo cost will be $0.05 - $0.50 maximum with proper setup! 