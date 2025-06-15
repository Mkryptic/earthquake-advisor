# 🌍 Disaster Ready: Earthquake Response Simulator

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![AWS Bedrock](https://img.shields.io/badge/AWS-Bedrock-orange.svg)](https://aws.amazon.com/bedrock/)

**AI-powered earthquake preparedness simulator for Southeast Asia with intelligent emergency response guidance.**

## 🎯 **Project Overview**

This simulator provides:
- **🤖 AI Emergency Advisor**: Natural language emergency response using AWS Bedrock
- **📚 Interactive Scenarios**: Realistic earthquake situations with scoring
- **🏥 Community Resources**: Emergency contacts, hospitals, evacuation centers
- **🌐 Multi-language Support**: English, Thai, Burmese
- **👥 Multi-Agent System**: Specialized emergency response coordination

## 🚀 **Quick Start**

### **Option 1: Zero-Cost Basic Version**
```bash
git clone https://github.com/Mkryptic/earthquake-advisor.git
cd earthquake-advisor
pip install -r requirements.txt
python simple_main.py
```
Visit: http://localhost:8000

### **Option 2: Full AI Version (AWS Required)**
```bash
# Set up AWS credentials (see setup guides)
.\setup_aws_credentials.ps1

# Start full AI version
python main.py
```

### **Option 3: Docker Deployment**
```bash
docker-compose up --build
```

## 📋 **Prerequisites**

### **Basic Version (Free)**
- Python 3.8+
- pip

### **AI Version (≤$0.50 cost)**
- AWS Account with Bedrock access
- API Keys configured
- Anthropic Claude models enabled

## 🔧 **Setup Guides**

| Guide | Purpose | Cost |
|-------|---------|------|
| `setup_aws_free.md` | Complete AWS setup with cost protection | $0.05-$0.50 |
| `get_api_keys.md` | Step-by-step API key creation | Free |
| `setup_aws_credentials.ps1` | Secure credential setup script | Free |
| `DEPLOYMENT.md` | Production deployment options | Varies |

## 🏗️ **Architecture**

```
├── agent/                  # AI Agents & Tools
│   ├── earthquake_advisor.py    # Main advisor agent
│   ├── multi_agent_coordinator.py # Agent coordination
│   └── tools.py           # Specialized emergency tools
├── data/                  # Emergency Resources
│   ├── community_data.json      # Hospitals, contacts, zones
│   └── scenarios.json     # Interactive earthquake scenarios
├── simulation/            # Scenario Engine
│   └── scenario_engine.py       # Simulation logic & scoring
├── main.py               # Full AI API server
├── simple_main.py        # Basic version (no AWS)
├── app.py               # Streamlit web interface
└── docker-compose.yml    # Container deployment
```

## 🌟 **Features**

### **🤖 AI Emergency Advisor**
- Natural language emergency guidance
- Situation-specific safety recommendations
- Building safety assessments
- Real-time emergency resource finder

### **📊 Interactive Scenarios**
- **Home Night Emergency**: 2:30 AM earthquake response
- **Office Building**: Workplace evacuation procedures
- **Shopping Mall**: Crowd management and exits
- **School Emergency**: Protecting children and evacuation
- **Driving Scenario**: Vehicle safety during earthquakes

### **🏥 Community Integration**
- **Thailand**: Bangkok hospitals, emergency services
- **Myanmar**: Yangon medical facilities, evacuation centers
- **Real Data**: Current emergency contacts and resources

### **👥 Multi-Agent System**
- **Medical Agent**: Injury assessment and first aid
- **Evacuation Agent**: Route planning and safety zones
- **Coordination Agent**: Resource allocation and communication

## 🔌 **API Endpoints**

### **Agent Endpoints**
- `POST /agent/chat` - Natural language emergency advisor
- `GET /agent/emergency-contacts/{location}` - Local emergency contacts
- `POST /agent/safety-advice` - Situation-specific guidance

### **Simulation Endpoints**
- `GET /simulation/scenarios` - Available earthquake scenarios
- `POST /simulation/start/{scenario_id}` - Begin interactive scenario
- `POST /simulation/answer` - Submit scenario responses

### **Educational Endpoints**
- `GET /education/safety-tips` - Earthquake preparedness tips
- `GET /education/supplies` - Emergency supply checklists

## 🚀 **Deployment Options**

### **1. Local Development**
```bash
python main.py  # Full AI version
python simple_main.py  # Basic version
```

### **2. Docker**
```bash
docker-compose up --build
```

### **3. AWS (Production)**
- **EC2**: Virtual machine deployment
- **ECS**: Container orchestration
- **App Runner**: Serverless deployment

See `DEPLOYMENT.md` for detailed instructions.

## 💰 **Cost Management**

### **Free Tier Usage**
- Basic version: $0
- AWS setup: Free tier eligible
- Development testing: Minimal cost

### **Production Usage**
- Claude 3 Haiku: $0.0001 per question
- Demo session: $0.05 - $0.50 maximum
- Monthly budget alerts configured

## 🔐 **Security**

- **Credential Management**: Environment variables only
- **Cost Protection**: Billing alerts and spending limits
- **API Security**: Rate limiting and input validation
- **Data Privacy**: No sensitive data storage

## 🌏 **Regional Focus**

### **Southeast Asia Earthquake Preparedness**
- **Thailand-Myanmar Border**: High seismic activity zone
- **Bangkok Metropolitan**: Urban earthquake response
- **Cultural Sensitivity**: Local emergency protocols
- **Language Support**: English, Thai, Burmese

## 🛠️ **Development**

### **Tech Stack**
- **Backend**: FastAPI + Python
- **AI**: AWS Bedrock (Anthropic Claude)
- **Frontend**: Streamlit
- **Data**: JSON-based emergency resources
- **Deployment**: Docker + AWS

### **Contributing**
1. Fork the repository
2. Create feature branch: `git checkout -b feature/new-feature`
3. Commit changes: `git commit -m 'Add new feature'`
4. Push to branch: `git push origin feature/new-feature`
5. Submit pull request

## 📚 **Documentation**

- **API Docs**: http://localhost:8000/docs (when running)
- **Setup Guides**: See individual `.md` files
- **Deployment**: `DEPLOYMENT.md`
- **AWS Setup**: `setup_aws_free.md`

## 🤝 **Support**

- **Issues**: [GitHub Issues](https://github.com/Mkryptic/earthquake-advisor/issues)
- **Documentation**: See setup guides in repository
- **AWS Costs**: Billing alerts configured automatically

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🎯 **Demo Ready**

This simulator is competition and demo ready with:
- ✅ Zero-cost basic version
- ✅ AI-powered intelligent responses
- ✅ Interactive scenario testing
- ✅ Production deployment options
- ✅ Comprehensive documentation
- ✅ Cost-effective AWS integration

---

**🚨 Emergency Preparedness Saves Lives - Be Ready! 🚨** 