# ScamShield AI — AWS EC2 Cloud Deployment Guide

This guide fulfills the optional **Cloud Deployment Bonus** by documenting how to deploy ScamShield AI onto a live AWS EC2 instance.

---

## 1. Quick Launch (Automated via User Data)

1. Open the [AWS EC2 Console](https://console.aws.amazon.com/ec2).
2. Click **Launch Instance**.
   - **Name**: `scamshield-ai-cloud`
   - **AMI**: `Ubuntu Server 24.04 LTS` or `22.04 LTS` (Free Tier eligible)
   - **Instance Type**: `t2.micro` or `t3.micro` (Free Tier eligible)
   - **Key Pair**: Select your existing key pair or create one.
3. **Network Settings (Security Group Rules)**:
   Ensure the following ports are open:
   | Port | Protocol | Source | Purpose |
   |:---:|:---:|:---:|---|
   | **22** | TCP | Your IP | Secure SSH administration |
   | **8000** | TCP | `0.0.0.0/0` | FastAPI Microservice & Swagger UI |
   | **8501** | TCP | `0.0.0.0/0` | Streamlit Cyber Defense Dashboard |

4. **Advanced Details -> User Data**:
   Paste the contents of [`deploy/aws/ec2-user-data.sh`](file:///Users/bhagyashreebhagat/Downloads/FeatureEnggAndMLOPs-main%202/ScamShield%20AI/deploy/aws/ec2-user-data.sh):
   ```bash
   #!/bin/bash
   apt-get update -y && apt-get install -y docker.io
   systemctl enable --now docker
   docker pull bhagyashreebhagat/scamshield-ai:latest
   docker run -d --name scamshield-ai-production --restart unless-stopped -p 8000:8000 -p 8501:8501 bhagyashreebhagat/scamshield-ai:latest
   ```
5. Click **Launch Instance**.
6. Within 2 minutes, access:
   - **Live UI**: `http://<EC2-PUBLIC-IP>:8501`
   - **Live API Docs**: `http://<EC2-PUBLIC-IP>:8000/docs`

---

## 2. Manual SSH Deployment (Alternative)

If you prefer to SSH in and run it manually:

```bash
# 1. SSH into the instance
ssh -i your-key.pem ubuntu@<EC2-PUBLIC-IP>

# 2. Install Docker
sudo apt update && sudo apt install -y docker.io
sudo usermod -aG docker ubuntu
newgrp docker

# 3. Pull and run image from Docker Hub
docker run -d -p 8000:8000 -p 8501:8501 --restart unless-stopped bhagyashreebhagat/scamshield-ai:latest

# 4. Verify healthy state
curl http://localhost:8000/health
```
