"""
Backyard Seed Advisor — Streamlit UI.

All controls in sidebar. All heavy logic in src/. Thin UI layer only.
"""

from __future__ import annotations
from datetime import datetime
from pathlib import Path

import streamlit as st

from src.models import (
    score_recommendation,
    get_current_season,
    REGIONS,
    SEASONS,
    COMMON_BIRDS,
    SEED_LABELS,
    get_bird_groups,
)
from src.plots import seed_score_bars, simple_coverage_pie
from src.export import (
    make_recipe_text,
    save_recipe_txt,
    save_scores_csv,
    save_excel,
)

st.set_page_config(
    page_title="Backyard Seed Advisor",
    page_icon="🐦",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Backyard Seed Advisor")
st.caption("Location + season + your sightings → ranked seeds + custom mix recipe. Pure client-side, no accounts, no uploads.")

# ---------------- Sidebar (all inputs live here) ----------------
with st.sidebar:
    st.header("Your Situation")

    default_season = get_current_season()
    season = st.selectbox(
        "Time of year",
        SEASONS,
        index=SEASONS.index(default_season),
        help="Affects fat vs. variety emphasis (suet & peanuts shine in winter).",
    )

    region = st.selectbox(
        "Region",
        REGIONS,
        index=REGIONS.index("National"),
        help="Adjusts for local bird tastes (e.g. milo is loved in the Southwest, often ignored in the Northeast).",
    )

    st.markdown("---")
    st.subheader("Birds you've seen recently")

    groups = get_bird_groups()
    selected: list[str] = []
    for grp, birds in groups.items():
        with st.expander(grp, expanded=(grp == "Cardinals & Grosbeaks")):
            for b in birds:
                if st.checkbox(b, key=f"bird_{b}"):
                    selected.append(b)

    # Free text for extras or less-common visitors
    extra = st.text_input(
        "Additional birds (comma-separated common names)",
        placeholder="e.g. Red-breasted Nuthatch, Purple Finch",
        help="We'll do a best-effort match against the known list.",
    )
    if extra.strip():
        for token in [t.strip() for t in extra.split(",") if t.strip()]:
            if token in COMMON_BIRDS and token not in selected:
                selected.append(token)
            # ignore unknowns for now (could add fuzzy later)

    if not selected:
        st.info("No birds selected — you'll get a balanced national/generic recommendation.")

    st.markdown("---")
    run_btn = st.button("Calculate recommendations", type="primary", use_container_width=True)

# ---------------- Main panel ----------------
if not run_btn:
    st.info("Set your region/season + check the birds you see, then click **Calculate recommendations** in the sidebar.")
    st.stop()

rec = score_recommendation(region, season, selected)

# Hero metrics
c1, c2, c3 = st.columns(3)
c1.metric("Top seed for you", rec["top_seeds"][0])
c2.metric("Best single addition", rec["top_seeds"][1] if len(rec["top_seeds"]) > 1 else "—")
c3.metric("Your birds strongly matched", f"{sum(1 for c in rec['bird_coverage'].values() if c['covered'])} / {len(rec['bird_coverage']) or 1}")

st.divider()

# Scores chart
st.subheader("Seed Match Scores")
fig = seed_score_bars(rec["scores_raw"], SEED_LABELS)
st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# Recipe
st.subheader("Custom Mix Recipe")
if rec["recipe"]:
    rec_df = [{"Seed": label, "% of mix": pct} for label, pct in rec["recipe"]]
    st.dataframe(rec_df, hide_index=True, use_container_width=True)
    st.caption("Proportions by weight. Offer in one large hopper or multiple feeders; adjust to what you can buy in bulk.")
else:
    st.write("Generic 50/50 black oil sunflower + white millet is a safe national default.")

# Your birds coverage
st.subheader("How well your birds are covered")
if rec["bird_coverage"]:
    cov_fig = simple_coverage_pie(rec["bird_coverage"])
    st.plotly_chart(cov_fig, use_container_width=True, config={"displayModeBar": False})

    with st.expander("Per-bird detail"):
        for bird, info in rec["bird_coverage"].items():
            emoji = "✅" if info["covered"] else "➕"
            st.write(f"{emoji} **{bird}** — best single seed: *{info['best_seed']}* (affinity {info['score']:.0f})")
else:
    st.write("Add sightings above for personalized coverage.")

# Downloads
st.subheader("Export")
col_dl1, col_dl2, col_dl3 = st.columns(3)

out_dir = Path("output")
out_dir.mkdir(exist_ok=True)

recipe_path = out_dir / "bird_seed_recipe.txt"
save_recipe_txt(rec, recipe_path)
with col_dl1:
    st.download_button(
        "📄 Recipe (txt)",
        data=recipe_path.read_text(encoding="utf-8"),
        file_name="bird_seed_recipe.txt",
        mime="text/plain",
    )

csv_path = out_dir / "seed_scores.csv"
save_scores_csv(rec, csv_path)
with col_dl2:
    st.download_button(
        "📊 Scores (csv)",
        data=csv_path.read_bytes(),
        file_name="seed_scores.csv",
        mime="text/csv",
    )

xlsx_path = out_dir / "bird_seed_recommendation.xlsx"
save_excel(rec, xlsx_path)
with col_dl3:
    st.download_button(
        "📈 Full report (xlsx)",
        data=xlsx_path.read_bytes(),
        file_name="bird_seed_recommendation.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

# Notes
if rec["notes"]:
    st.subheader("Notes & caveats")
    for n in rec["notes"]:
        st.warning(n) if "ignored" in n.lower() or "blackbird" in n.lower() else st.info(n)

# Help
with st.expander("Help & tips (plain language)"):
    st.markdown(
        """
**How to use the results**
- Put the top 1–2 seeds in separate feeders so finicky birds can choose.
- A "custom mix" is great for a big hopper, but many people do better offering 2–3 pure seeds in different feeder styles.
- Nyjer and hearts need specialized ports (finches have tiny beaks).

**Feeder quick guide**
- Tube/sock: nyjer, hearts, small sunflower
- Hopper/platform: sunflower, safflower, millet, peanuts
- Suet cage: suet (and peanuts in winter)
- Ground or low tray: millet, cracked corn (expect doves + squirrels)

**Data notes**
Scores come from published feeder preference studies (Cornell, Audubon, Kaytee, Avian Report). Regional/season multipliers are adjustments on top of those base affinities. Your actual yard may vary with cover, water, predators, and what the neighbors are offering.

**No eBird key?**
Export your personal sightings from eBird (My Data → Download) and paste the species names. Core tool never phones home.
"""
    )

st.caption(f"Generated {datetime.now().isoformat(timespec='seconds')} | Backyard Seed Advisor (bird-seed-recommender)")