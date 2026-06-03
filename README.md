# Backyard Seed Advisor

*Recommends optimal wild bird seed types and custom mixes from your location, season, and recent sightings.*

A simple, private, client-side tool. No accounts, no uploads, no cloud calls for the core experience.

---

## Live App

Once deployed, the interactive version lives at a URL like:

https://bird-seed-recommender-XXXX.streamlit.app

### Deploy steps (one time)
1. Push your code (already done for the scaffold).
2. Go to https://share.streamlit.io (Streamlit Community Cloud) and sign in with the GitHub account that owns the altustd org/repo.
3. Click **New app** (or Deploy an app).
4. Choose "I have a GitHub repo" / connect the `altustd/bird-seed-recommender` repository.
5. Main branch.
6. **Main file path**: `app.py` (preferred, our primary source) **or** `streamlit_app.py` (we added a thin compatibility wrapper so the common Streamlit Cloud default also works).
   - If the form shows "streamlit_app.py This file does not exist", just change the value to `app.py`.
7. (Optional) Set a custom subdomain/slug if available.
8. Deploy. The first build will pip install from `requirements.txt` (we added it for cloud compatibility; pixi.toml + `pixi run app` is for your local full conda environment).

The app will auto-redeploy on future `git push` to main.

Repo: https://github.com/altustd/bird-seed-recommender

After deploy, tell the AI the exact URL so the website cards and docs can be updated from the XXXX placeholder. (The "New" badge is already on the card on www.troyaltus.com once pushed.)

## Run Locally

```bash
cd tools/bird-seed-recommender
pixi install
pixi run setup          # one-time: register Jupyter kernel
pixi run app            # Streamlit UI (sidebar controls, instant recs + charts)
pixi run cli -- --help  # scriptable version
pixi run test
```

## What it does
- Takes your US region (or generic), season, and list of birds you've actually seen at your feeders.
- Scores 9 seed types (black oil sunflower, nyjer, safflower, millet, peanuts, suet, hearts, cracked corn, milo) using curated affinity tables + regional/seasonal adjustments.
- Suggests a proportional custom mix recipe + top single seeds to offer.
- Shows which of *your* birds are well covered and gives plain-language tips.

## Tech Stack
Python · Streamlit · pandas · Plotly · pixi

## Data
Hardcoded affinities synthesized from Cornell Lab of Ornithology (All About Birds), Kaytee, Audubon, and Avian Report feeder studies. See `src/data.py` for sources and exact values.

## License / Use
Personal use encouraged. Cite the sources in `src/data.py` if you share derived tables.
