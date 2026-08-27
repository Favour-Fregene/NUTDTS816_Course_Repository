# Data snapshots

PROVENANCE STATEMENT (updated 25 Aug 2026): the Nigerian series in this directory are a mix of REAL official snapshots
and two deliberately SIMULATED stand-ins. Each file's .PROVENANCE.txt sidecar is authoritative - quote it in any work
that uses the series.

REAL (official snapshots, downloaded 24-25 Aug 2026; full extraction detail in ../raw/EXTRACTION_NOTES.md):
nigeria_cpi (NBS, spliced across the Jan 2025 rebasing), nigeria_fx (CBN daily official rate, monthly means),
nigeria_grid (Ember monthly generation), bonny_light (CBN), daily_demand (PJM, US EIA-930),
nigeria_covid (WHO weekly), nigeria_rain_obs (NASA POWER).

SIMULATED (course-generated, seeded, by design - see each sidecar for why):
nigeria_malaria and nigeria_rainfall - the internally consistent Case Study 2 pair.

Textbook series (real): airpassengers, a10, h02, ausbeer, elecequip, usmelec, uschange, goog, dax, nile, austourists,
oil, elecdemand.

All files: a `date` column (ISO dates) plus one value column named as in `src/tsdata.py`; `goog` and `dax` are indexed
by trading day. ../raw/ holds the two-column source extracts the Nigerian snapshots were built from.
