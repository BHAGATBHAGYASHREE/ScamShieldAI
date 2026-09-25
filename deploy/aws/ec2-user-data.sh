#!/bin/bash
# deploy/aws/ec2-user-data.sh
#
# EC2 User Data Bootstrap Script for ScamShield AI
# Launches directly on an AWS EC2 instance (Ubuntu 22.04 LTS, t2.micro or t3.micro Free Tier)
# Installs Docker, pulls the published image from Docker Hub, and starts the container.

set -euo pipefail

IMAGE="bhagyashreebhagat/scamshield-ai:latest"
CONTAINER_NAME="scamshield-ai-production"

echo "[ScamShield AWS Setup] Updating system packages..."
apt-get update -y
apt-get install -y docker.io

echo "[ScamShield AWS Setup] Enabling and starting Docker daemon..."
systemctl enable docker
systemctl start docker

# Allow default ubuntu user to run docker
usermod -aG docker ubuntu || true

echo "[ScamShield AWS Setup] Pulling production image: ${IMAGE}..."
docker pull "${IMAGE}"

echo "[ScamShield AWS Setup] Launching ScamShield AI container..."
docker run -d \
    --name "${CONTAINER_NAME}" \
    --restart unless-stopped \
    -p 8000:8000 \
    -p 8501:8501 \
    "${IMAGE}"

echo "[ScamShield AWS Setup] Deployment complete!"
echo "API Docs: http://<PUBLIC-IP>:8000/docs"
echo "Streamlit UI: http://<PUBLIC-IP>:8501"
