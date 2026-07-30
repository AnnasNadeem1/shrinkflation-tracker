# Shrinkflation Tracker 🛒

A lightweight pipeline that tracks the **price per gram** of snack products sold by Greenvalley Grocery (RWP) over time, to help spot shrinkflation — when a product's price stays flat but its weight quietly shrinks.

## How It Works

1. **`script.py`** hits Greenvalley's public product JSON endpoint (`/collections/snacks/products.json`), pulls out each product's title and price, and parses the weight (g, ml, kg, or oz) out of the title using regex. It normalizes everything to grams, computes `Price_Per_Gram`, and saves the result as a dated CSV snapshot (e.g. `greenvalley_snacks_2026-07-26.csv`).
2. **Weekly snapshots** are committed to the repo, building up a time series you can compare week over week to see when a product's weight drops while its price stays the same.
3. **`dashboard.py`** is a Streamlit app that loads a snapshot and gives you:
   - Headline metrics (products tracked, highest/lowest price per gram)
   - A searchable, formatted table of products
   - An interactive Plotly bar chart of the top 20 most expensive items by price per gram
4. **GitHub Actions** (`.github/workflows/`) runs the scraper on a schedule to keep the snapshots current.

## Tech Stack

- **Python** — `requests`, `pandas`, `re` for scraping and data cleaning
- **Streamlit** + **Plotly** for the interactive dashboard
- **GitHub Actions** for scheduled automation

## Getting Started

### 1. Clone the repo

```bash
git clone https://github.com/AnnasNadeem1/shrinkflation-tracker.git
cd shrinkflation-tracker
```

### 2. Install dependencies

```bash
pip install requests pandas streamlit plotly
```

### 3. Run the scraper

```bash
python script.py
```

This fetches the latest data and saves a new `greenvalley_snacks_<date>.csv` file.

### 4. Launch the dashboard

```bash
streamlit run dashboard.py
```

Then open `http://localhost:8501` in your browser.

> **Note:** `dashboard.py` currently loads `greenvalley_snacks_may_2026.csv` by default — update the filename in `load_data()` if you want to view a different snapshot.

## Data

Each snapshot CSV includes:

| Column | Description |
|---|---|
| Product Name | Raw product title from Greenvalley |
| Price (PKR) | Listed price in Pakistani Rupees |
| Weight | Parsed numeric weight |
| Unit | Parsed unit (g, ml, kg, oz) |
| Weight_Grams | Weight normalized to grams |
| Price_Per_Gram | Price ÷ Weight_Grams — the core shrinkflation signal |

## Planned Analysis & Forecasting

The weekly snapshots are being collected specifically to support deeper analysis down the line:

- **Historical trend analysis** — merge all `greenvalley_snacks_*.csv` files into a single time-series dataset keyed by product, and track how `Weight_Grams` and `Price_Per_Gram` move independently over time.
- **Shrinkflation event detection** — flag products where price stays flat (or rises) while `Weight_Grams` drops between consecutive snapshots, and quantify the effective price increase this represents.
- **Inflation correlation** — pull in Pakistan's official CPI / food inflation data (e.g. from PBS or SBP) and compare it against the price-per-gram trend to see whether shrinkflation tends to substitute for, lag, or amplify headline inflation.
- **Forecasting** — use the growing time series to model and predict future price-per-gram trajectories per product or category (e.g. simple regression or time-series models like ARIMA/Prophet as a starting point), to anticipate likely shrinkflation before it's officially visible on shelves.
- **Category/brand-level rollups** — aggregate beyond individual SKUs to see which brands or categories are shrinking fastest.

This will likely mean moving from flat CSVs to a proper time-series-friendly storage format (e.g. a single consolidated dataset or lightweight database) as more weekly snapshots accumulate.

## Roadmap Ideas

- Automate the diffing of snapshots to flag shrinkflation events without manual review
- Store snapshots in a database instead of flat CSVs for easier historical querying
- Add alerting (e.g. Discord/Slack webhook) when a shrinkflation event is detected
- Build out the inflation-correlation and forecasting analysis described above
- Expand beyond the snacks category

## License

Add a license of your choice (e.g. MIT) if you plan to make this public.
