# ScamShield AI — Render Cloud Deployment Guide

This guide details how to deploy ScamShield AI onto **Render.com** (100% Free Tier, zero credit card required).

---

## Method 1: Deploy Directly from Docker Hub (Fastest, ~2 Minutes)

Because our GitHub Actions CI/CD has already built and published the production image to Docker Hub, you can deploy without rebuilding:

1. Log into your account at [dashboard.render.com](https://dashboard.render.com).
2. Click **New +** (top right) and choose **Web Service**.
3. Under **Deploy an existing image**, click **Next**.
4. Enter the Docker Image URL:
   ```text
   docker.io/bhagyashreebhagat/scamshield-ai:latest
   ```
5. Click **Next** and configure:
   - **Name:** `scamshield-ai`
   - **Region:** Any (e.g. `Singapore` or `Oregon`)
   - **Instance Type:** `Free`
6. Under **Advanced** &rarr; **Add Environment Variable**:
   - `PORT` = `8501`
   - `API_URL` = `http://127.0.0.1:8000`
7. Click **Create Web Service**.
8. Render pulls the container and boots both FastAPI and Streamlit.
   - Your live public URL will be ready at: **`https://scamshield-ai.onrender.com`**

---

## Method 2: Deploy from GitHub Repository (Auto-Sync on Push)

1. Go to [dashboard.render.com/blueprints](https://dashboard.render.com/blueprints).
2. Click **New Blueprint Instance**.
3. Connect your GitHub repository: `BHAGATBHAGYASHREE/ScamShieldAI`.
4. Render will detect [`render.yaml`](../../render.yaml) automatically.
5. Click **Apply**. Render will automatically build the `Dockerfile` and deploy the service.

---

## Verifying Deployment

Once the service shows **Live** (green status) in the Render dashboard:
- **Streamlit Web UI:** `https://scamshield-ai.onrender.com`
- **FastAPI Health Check:** Visit the Web Service and inspect the health status.
