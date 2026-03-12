# Deploy Backend to Render – Step by Step

Deploy the Insurance Fraud & Severity Flask app as a **Web Service** on [Render](https://render.com).

---

## Before you start

- Have a [Render account](https://dashboard.render.com/register) (free tier is enough).
- Put your code in a **Git repository** (GitHub, GitLab, or Bitbucket). If it’s not there yet:
  1. Create a new repo on GitHub.
  2. In your project folder run:
     ```bash
     git init
     git add .
     git commit -m "Initial commit"
     git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
     git branch -M main
     git push -u origin main
     ```

---

## Step 1: Open Render dashboard

1. Go to [https://dashboard.render.com](https://dashboard.render.com).
2. Log in.

---

## Step 2: Create a new Web Service

1. Click **New +**.
2. Choose **Web Service**.
3. Connect your Git provider (GitHub / GitLab / Bitbucket) if asked, and **authorize Render**.
4. Select the repository that contains your **ML Project** (the one with `app.py`, `requirements.txt`, etc.).
5. Click **Connect**.

---

## Step 3: Configure the Web Service

Use these settings (adjust if your repo name or branch is different):

| Field | Value |
|--------|--------|
| **Name** | `insurance-fraud-app` (or any name you like) |
| **Region** | Choose the closest to your users |
| **Branch** | `main` (or your default branch) |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app:app --bind 0.0.0.0:$PORT` (or leave blank to use the Procfile) |

---

## Step 4: Environment variables (recommended)

1. In the same page, open the **Environment** section.
2. Add at least:

| Key | Value | Notes |
|-----|--------|--------|
| `SECRET_KEY` | A long random string | e.g. generate with `python -c "import secrets; print(secrets.token_hex(32))"` |
| `PYTHON_VERSION` | `3.11.9` (full version required) | Only if you set it: use major.minor.patch (e.g. `3.11.9`). Or omit and use `.python-version` in the repo. |

Optional (for local-style debugging; **do not use in production**):

| Key | Value |
|-----|--------|
| `FLASK_DEBUG` | `false` |

Save the env vars.

---

## Step 5: Deploy

1. Click **Create Web Service**.
2. Render will clone the repo, run `pip install -r requirements.txt`, and start the app with `gunicorn app:app`.
3. Wait for the first deploy to finish (build + start). The log will show a URL like `https://insurance-fraud-app.onrender.com`.

---

## Step 6: Open the app

1. Click the generated URL (e.g. `https://your-service-name.onrender.com`) or open it in a browser.
2. You should see the app (login/register if your app has it).
3. **Important:** On the free tier, the app **spins down after ~15 minutes** of no traffic. The next request may take 30–60 seconds to wake it up.

---

## Data and models on Render

- The server filesystem is **ephemeral**: anything written to `uploads/` or `trained_models/` is lost on redeploy or restart.
- So:
  - **Option A:** Commit a **default dataset** (e.g. `insurance_claims_fraud.csv`) and optionally **pre-trained models** (`trained_models/full_store.pkl`) in the repo so they’re present after each deploy.
  - **Option B:** After each deploy, upload the CSV and (if your app supports it) retrain so models are generated again.

To use Option A:

1. Put `insurance_claims_fraud.csv` in `uploads/` in the repo.
2. (Optional) Run `train_and_save_models.py` locally, then commit the contents of `trained_models/` (e.g. `full_store.pkl`) into the repo so the app can load them on start.

---

## Troubleshooting

| Issue | What to do |
|--------|------------|
| Build fails | Check the **Build logs** for missing dependencies or wrong Python version. If you set `PYTHON_VERSION`, use full version (e.g. `3.11.9`). Ensure `requirements.txt` is in the repo and has no typos. |
| App crashes at start | Check **Logs** for Python errors. Ensure `SECRET_KEY` is set and that the start command is `gunicorn app:app` (or `python app.py`). |
| 503 / “Application failed to start” | Same as above; also confirm the app listens on `0.0.0.0` and uses the `PORT` env var (the app code already does this). |
| Slow first request | Normal on free tier after idle spin-down; the instance is waking up. |

---

## Summary checklist

- [ ] Code in a Git repo (GitHub/GitLab/Bitbucket).
- [ ] Repo connected to Render and Web Service created.
- [ ] Build command: `pip install -r requirements.txt`.
- [ ] Start command: `gunicorn app:app` (or leave blank if using Procfile).
- [ ] `SECRET_KEY` (and optionally `PYTHON_VERSION` = full version e.g. `3.11.9`) set in Environment.
- [ ] Default data/models in repo or plan to re-upload/re-train after deploy.

After that, every push to the connected branch will trigger a new deploy on Render.
