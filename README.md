# NUTDTS 816 Time Series Analysis — Course Repository

**Nigerian University of Technology and Management (NUTM) · MSc Data Science · September–December 2026**
**Instructor:** Dr Tolulope Adesina · toadesina@ieee.org

This repository holds everything students need to run the course labs: the 25 lab notebooks (one per session), the
course data module `src/tsdata.py`, and snapshot datasets in `data/`. Nothing needs installing locally; every notebook
runs in Google Colab from the "Open in Colab" badge (or by uploading the `.ipynb`).

## Layout

```
notebooks/   lab00_familiarisation.ipynb … lab24_synthesis_and_examination_preparation.ipynb
src/         tsdata.py      the data module used by every notebook and by the lecture notes
data/        CSV snapshots: Nigerian series (simulated placeholders until the real snapshots are dropped in) and the
             textbook series (real, cached from the fpp2 / base-R collections so labs do not depend on live downloads)
docs/        redacted
requirements.txt
```

## Running a lab in Colab

1. Open the notebook in Colab (File > Upload notebook, or the badge once the repository is public).
2. Edit the `REPO` line in the setup cell to point at this repository's raw URL, e.g.
   `https://raw.githubusercontent.com/<user>/nutdts816/main`.
3. Run the setup cell (about two minutes the first time: it installs the libraries and downloads `tsdata.py` and the data).
4. Work through the cells. Each notebook is self-contained: the even-numbered labs begin by re-running the code they
   inherit from the previous session.

Labs 17 and 18 train neural networks (NHITS takes a few minutes on the free Colab CPU; switch the runtime to a T4 GPU
to speed it up). Lab 18's Chronos and TimeGPT cells need `pip install chronos-forecasting` and an internet connection to
download model weights.

## The Nigerian data

The notebooks and the lecture notes use the Nigerian series below. As of 25 August 2026 the shipped CSVs are **real
official snapshots** for seven series; `nigeria_malaria` and `nigeria_rainfall` are **deliberately simulated** as the
internally consistent Case Study 2 pair (state-level NCDC weekly malaria counts are not publicly downloadable, and the
case study's rainfall-lead and outbreak design requires a pair with known structure). Every file has a
`.PROVENANCE.txt` sidecar, which is authoritative and must be quoted in any work that uses the series. The two-column
source extracts and the full extraction log live in `raw/`.

| File | Columns | Source (snapshot) | Span | Status |
|---|---|---|---|---|
| `nigeria_cpi.csv` | `date, cpi` | NBS all-items CPI, spliced across the Jan 2025 rebasing (2024 = 100 basis) | Jan 2014 – Dec 2025 | REAL |
| `nigeria_fx.csv` | `date, ngn_usd` | CBN daily official Central Rate, monthly means (official window throughout) | Jan 2015 – Jul 2026 | REAL |
| `nigeria_grid.csv` | `date, generation_mw` | Ember Monthly Electricity Data, Nigeria total generation (avg MW) | Jan 2019 – Apr 2026 | REAL |
| `bonny_light.csv` | `date, bonny_light` | CBN crude oil statistics, monthly average USD/bbl | Jan 2015 – Jun 2026 | REAL |
| `daily_demand.csv` | `date, demand_gwh` | PJM Interconnection daily demand (US EIA-930); US holidays apply | Jan 2022 – Aug 2026 | REAL |
| `nigeria_covid.csv` | `date, cases` | WHO weekly confirmed COVID-19 cases, Nigeria | Mar 2020 – Jan 2023 | REAL |
| `nigeria_rain_obs.csv` | `date, rain_mm` | NASA POWER (MERRA-2) monthly rainfall, NE-Nigeria regional mean | Jan 2019 – Dec 2025 | REAL |
| `nigeria_malaria.csv` | `date, cases` | Course-generated weekly series in the shape of NCDC state surveillance | 2019 – Jun 2026 | SIMULATED |
| `nigeria_rainfall.csv` | `date, rain_mm` | Course-generated monthly rainfall, the pair for `nigeria_malaria` | 2019 – Jun 2026 | SIMULATED |

Two features of the real data every user should know: the CPI carries the NBS rebasing seam at January 2025 (a
published −2.8% month-on-month step that is methodological, not deflation — see the provenance sidecar), and the FX
series follows the official window throughout, so the pre-2023 pegged plateaus are real regime features, not data
errors.

Fallback sources actually used where portals were unavailable: NBS tables workbooks (CPI), BIS / World Bank GEM
(exchange-rate cross-checks), Ember (grid), WHO (weekly cases), US EIA (daily demand), NASA POWER (rainfall), World
Bank Global Database of Inflation (CPI verification).

Setting the environment variable `NUTDTS816_DATA` points `tsdata.py` at a different data directory.

## Libraries

`pandas`, `numpy`, `matplotlib`, `plotly`, `statsmodels`, `pmdarima`, `statsforecast`, `neuralforecast`, `scikit-learn`,
`lightgbm`, `torch`, `arch`; optional `chronos-forecasting`, `nixtla`. See `requirements.txt`.

## Licence and citation

Course materials © 2026 Tolulope Adesina, for use in NUTDTS 816. Textbook datasets are from Hyndman and Athanasopoulos,
*Forecasting: Principles and Practice* (CC BY-NC-SA) and base R (GPL). Students' project repositories must include their
own licence and a data-provenance statement.
