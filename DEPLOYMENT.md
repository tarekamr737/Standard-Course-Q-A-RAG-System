# GitHub and Streamlit Community Cloud deployment

## Publish to GitHub

1. Confirm that `.env`, `.streamlit/secrets.toml`, `data/uploads/`, `data/index/`, and real course PDFs are not staged. The AI-Based Programming PDFs are intentionally ignored so they remain local on `D:`.
2. Review the staged changes, then commit and push the `main` branch:

```powershell
git status
git add .
git diff --cached
git commit -m "Prepare CourseGround for Streamlit Community Cloud"
git remote add origin https://github.com/YOUR-ACCOUNT/YOUR-REPOSITORY.git
git push -u origin main
```

Do not run `git add .` until the staged-file review shows no private course materials or secrets.

## Deploy to Streamlit Community Cloud

1. Sign in at [Streamlit Community Cloud](https://share.streamlit.io/) and connect the GitHub account that owns the repository.
2. Select **Create app**, then choose the repository, the `main` branch, and `app.py` as the entrypoint.
3. Open **Advanced settings** and choose Python 3.11, which matches the local test environment.
4. Copy the contents of `.streamlit/secrets.toml.example` into the **Secrets** field, replacing `OPENROUTER_API_KEY` with your real key and selecting the models you intend to use.
5. Deploy. Once it launches, upload any non-public course materials through the app and rebuild that course index.

## Deployment behavior

- `requirements.txt` is in the repository root, alongside `app.py`.
- `.streamlit/config.toml` is committed at the repository root.
- Root-level Community Cloud secrets are available to CourseGround as environment variables.
- The app creates indexes, uploaded files, and custom courses at runtime. Treat these as rebuildable data and keep original course materials backed up outside the deployment.
