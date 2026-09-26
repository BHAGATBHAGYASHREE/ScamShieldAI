# FAARZI AI — Render Cloud Deployment Guide (Native Python — No Docker)

This guide details how to deploy FAARZI AI on **Render.com** using the native **Python 3 Web Service** environment (100% Free Tier, zero Docker required).

---

## Method 1: Web Service via Render Dashboard (Recommended)

1. Log into your account at [dashboard.render.com](https://dashboard.render.com).
2. Click **New +** (top right) &rarr; choose **Web Service**.
3. Under **Connect a repository**, select:
   ```text
   BHAGATBHAGYASHREE/ScamShieldAI
   ```
4. Configure the service parameters:
   - **Name:** `faarzi-ai`
   - **Language / Runtime:** `Python 3` *(NOT Docker)*
   - **Branch:** `main`
   - **Region:** Any (e.g. `Oregon` or `Singapore`)
   - **Instance Type:** `Free`

5. **Build & Start Commands:**
   - **Build Command:**
     ```bash
     pip install --upgrade pip && pip install -r requirements.txt
     ```
   - **Start Command:**
     ```bash
     bash entrypoint.sh
     ```
     *(Runs both the FastAPI microservice on port 8000 and the Streamlit UI bound to `$PORT` automatically).*

     > **Alternative (Streamlit Standalone with local pipeline):**
     > If you only want Streamlit without the FastAPI background daemon:
     > ```bash
     > streamlit run streamlit_app.py --server.port $PORT --server.address 0.0.0.0 --server.enableCORS false --server.enableXsrfProtection false
     > ```

6. **Environment Variables:**
   Under **Advanced** &rarr; **Add Environment Variable**:
   - `PYTHON_VERSION` = `3.11.9`
   - `API_URL` = `http://127.0.0.1:8000`

7. Click **Create Web Service**.
8. Render will install dependencies via pip, boot the application, and assign a free HTTPS URL:
   - **Live Public URL:** `https://faarzi-ai.onrender.com`

---

## Method 2: One-Click Blueprint Deployment (`render.yaml`)

Because [`render.yaml`](../../render.yaml) is already configured for native Python:

1. Go to [dashboard.render.com/blueprints](https://dashboard.render.com/blueprints).
2. Click **New Blueprint Instance**.
3. Select your repository: `BHAGATBHAGYASHREE/ScamShieldAI`.
4. Render automatically parses `render.yaml` with the native Python runtime, build command, and start command.
5. Click **Apply**.

---

## Verifying Deployment

Once the service shows **Live** (green status):
- **Streamlit Web UI:** `https://<your-service-name>.onrender.com`
- **FastAPI Health Check:** Visit `http://127.0.0.1:8000/health` (internal) or check deployment logs.

