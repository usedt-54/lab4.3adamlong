# Submission checklist and reflection draft

## Deploy (about 10 minutes)

1. Create a new **public** repo on GitHub, e.g. `online-orders-dashboard`.
2. Upload this whole folder (`app.py`, `requirements.txt`, `data/online_orders.csv`, `README.md`, `PLAN.md`, `wireframe.svg`).
   On github.com: **Add file → Upload files**, drag everything in (keep the `data/` folder), then **Commit**.
3. Go to https://share.streamlit.io, sign in with GitHub, choose **Create app → Deploy a public app from GitHub**.
4. Pick the repo, branch `main`, main file `app.py`, then **Deploy**.
5. Paste the app URL into `README.md` and into your submission.

## Section 1 (submit separately)

- Goal and audience, 3–4 questions with columns and chart types → `PLAN.md`
- Wireframe image → open `wireframe.svg` in a browser and take a screenshot
- Gallery-walk votes → fill in the table at the end of `PLAN.md` after looking at the designs in Teams

## Section 2

- Streamlit app URL
- GitHub repo link
- Reflection paragraph (below)

## Reflection draft — edit this so it's accurate and in your own words

> I worked on this project alone, so I did the planning, building, and testing myself. The app follows my wireframe closely: a sidebar of filters (date range, category, region, device, customer type), a row of five KPI cards, a monthly revenue line chart, and bar charts for my other three questions. A few things changed during the build. I first planned to write the insights by hand, but I made them compute from the filtered data, so they stay correct when the filters change. I also moved the value labels inside the bars after I found that dark text above the bars disappeared in Streamlit's dark theme, and I fixed the rating chart's axis at 0–5 so a one-star gap isn't exaggerated. The main design principle I applied was not relying on color alone: every bar uses the same color, and the meaning comes from printed values, axis titles with units (USD, %, stars) and a caption under each chart. I used an AI assistant (Claude) to [describe honestly — e.g. "generate the first version of the code and the wireframe, which I then reviewed, tested with different filters and adjusted"].
