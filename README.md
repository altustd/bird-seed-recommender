# Backyard Seed Advisor

*Recommends optimal wild bird seed types and custom mixes from your location, season, and recent sightings.*

A simple, private, client-side tool. No accounts, no uploads, no cloud calls for the core experience.

---

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
