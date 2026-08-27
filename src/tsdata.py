"""tsdata.py - datasets for NUTDTS 816 Time Series Analysis (NUTM MSc Data Science).

Every loader first looks for a CSV snapshot in DATA_DIR (default ./data), with columns `date` and the series name.
If the file is absent it falls back to (a) the Rdatasets mirror for the textbook series or (b) a SIMULATED series for the
Nigerian data. To use the real NBS / CBN / EIA / NERC-TCN / NCDC / NiMet series, drop CSVs with the same names into
data/ (see data/README.md for provenance and format); nothing in the notebooks changes.

Columns expected in data/<name>.csv:
  nigeria_cpi.csv       date, cpi            monthly, month start, all-items CPI (NBS)
  nigeria_fx.csv        date, ngn_usd        monthly average official NGN/USD (CBN)
  nigeria_grid.csv      date, generation_mw  monthly average grid generation, MW (NERC / TCN / NSO)
  nigeria_malaria.csv   date, cases          weekly confirmed cases, epi-week ending Sunday (NCDC)
  nigeria_rainfall.csv  date, rain_mm        monthly rainfall, mm (NiMet or NASA POWER)
  bonny_light.csv       date, bonny_light    monthly average spot price, USD/bbl (EIA)
  daily_demand.csv      date, demand_gwh     daily electricity demand, GWh (PJM, US EIA-930)
  nigeria_covid.csv     date, cases          weekly confirmed COVID-19 cases, week ending Sunday (WHO) - REAL, local only
  nigeria_rain_obs.csv  date, rain_mm        observed monthly rainfall, mm (NASA POWER) - REAL, local only

As of 25 Aug 2026 the shipped snapshots are REAL for cpi, fx, grid, bonny_light, daily_demand, covid and rain_obs;
nigeria_malaria and nigeria_rainfall remain the deliberately SIMULATED Case Study 2 pair (see data/*.PROVENANCE.txt).
"""
import os
import numpy as np, pandas as pd

DATA_DIR = os.environ.get('NUTDTS816_DATA', 'data')

def _local(name, col=None, freq=None, index_col='date'):
    path = os.path.join(DATA_DIR, f'{name}.csv')
    if not os.path.exists(path): return None
    df = pd.read_csv(path)
    if index_col in df.columns:
        df[index_col] = pd.to_datetime(df[index_col]); df = df.set_index(index_col)
        if freq: df = df.asfreq(freq)
    else:
        df = df.set_index(df.columns[0])
    if col is None: col = [c for c in df.columns][0]
    s = df[col] if col in df.columns else df.iloc[:, 0]
    return s if isinstance(s, pd.Series) else s

def _rd(name, pkg):
    import statsmodels.api as sm
    return sm.datasets.get_rdataset(name, pkg, cache=True).data

def _ts_monthly(df, start): return pd.Series(df['value'].values, index=pd.date_range(start, periods=len(df), freq='MS'))
def _ts_quarterly(df, start): return pd.Series(df['value'].values, index=pd.period_range(start, periods=len(df), freq='Q').to_timestamp())

# ---------------- textbook series (real) ----------------
def airpassengers():
    s = _local('airpassengers', 'passengers', 'MS')
    if s is None: s = _ts_monthly(_rd('AirPassengers', 'datasets'), '1949-01-01')
    s.name = 'passengers'; return s

def a10():
    s = _local('a10', 'a10', 'MS')
    if s is None: s = _ts_monthly(_rd('a10', 'fpp2'), '1991-07-01')
    s.name = 'a10'; return s

def h02():
    s = _local('h02', 'h02', 'MS')
    if s is None: s = _ts_monthly(_rd('h02', 'fpp2'), '1991-07-01')
    s.name = 'h02'; return s

def ausbeer():
    s = _local('ausbeer', 'beer', 'QS')
    if s is None: s = _ts_quarterly(_rd('ausbeer', 'fpp2'), '1956Q1')
    s.name = 'beer'; return s

def elecequip():
    s = _local('elecequip', 'elecequip', 'MS')
    if s is None: s = _ts_monthly(_rd('elecequip', 'fpp2'), '1996-01-01')
    s.name = 'elecequip'; return s

def usmelec():
    s = _local('usmelec', 'usmelec', 'MS')
    if s is None: s = _ts_monthly(_rd('usmelec', 'fpp2'), '1973-01-01')
    s.name = 'usmelec'; return s

def uschange():
    path = os.path.join(DATA_DIR, 'uschange.csv')
    if os.path.exists(path):
        df = pd.read_csv(path, parse_dates=['date']).set_index('date'); return df.asfreq('QS')
    df = _rd('uschange', 'fpp2'); df.index = pd.period_range('1970Q1', periods=len(df), freq='Q').to_timestamp(); return df

def goog():
    path = os.path.join(DATA_DIR, 'goog.csv')
    if os.path.exists(path):
        df = pd.read_csv(path); return pd.Series(df['goog'].values, index=pd.RangeIndex(1, len(df) + 1), name='goog')
    df = _rd('goog', 'fpp2'); return pd.Series(df['value'].values, index=pd.RangeIndex(1, len(df) + 1), name='goog')

def dax():
    path = os.path.join(DATA_DIR, 'dax.csv')
    if os.path.exists(path):
        df = pd.read_csv(path); return pd.Series(df['dax'].values, index=pd.RangeIndex(1, len(df) + 1), name='dax')
    df = _rd('EuStockMarkets', 'datasets'); return pd.Series(df['DAX'].values, index=pd.RangeIndex(1, len(df) + 1), name='dax')

def elecdemand():
    path = os.path.join(DATA_DIR, 'elecdemand.csv')
    if os.path.exists(path):
        df = pd.read_csv(path, parse_dates=['date']).set_index('date'); return df.asfreq('30min')
    df = _rd('elecdemand', 'fpp2'); df.index = pd.date_range('2014-01-01', periods=len(df), freq='30min'); return df

def nile():
    s = _local('nile', 'nile', 'YS')
    if s is None:
        df = _rd('Nile', 'datasets'); s = pd.Series(df['value'].values, index=pd.date_range('1871-01-01', periods=len(df), freq='YS'))
    s.name = 'nile'; return s

def austourists():
    s = _local('austourists', 'tourists', 'QS')
    if s is None: s = _ts_quarterly(_rd('austourists', 'fpp2'), '1999Q1')
    s.name = 'tourists'; return s

def oil():
    s = _local('oil', 'oil', 'YS')
    if s is None:
        df = _rd('oil', 'fpp2'); s = pd.Series(df['value'].values, index=pd.date_range('1965-01-01', periods=len(df), freq='YS'))
    s.name = 'oil'; return s

# ---------------- Nigerian series: local snapshot first, else SIMULATED ----------------
def nigeria_cpi(seed=816):
    s = _local('nigeria_cpi', 'cpi', 'MS')
    if s is not None: s.name = 'cpi'; return s
    rng = np.random.default_rng(seed)
    idx = pd.date_range('2015-01-01', '2026-06-01', freq='MS'); n = len(idx)
    ann = np.where(idx < '2020-06-01', 0.12, np.where(idx < '2023-06-01', 0.17, np.where(idx < '2025-01-01', 0.31, 0.22)))
    monthly = np.log1p(ann) / 12; season = 0.004 * np.sin(2 * np.pi * (idx.month - 5) / 12)
    shock = np.zeros(n); shock[(idx >= '2023-06-01') & (idx < '2023-09-01')] = 0.012
    lcpi = np.log(180) + np.cumsum(monthly + shock + rng.normal(0, 0.004, n)) + season
    return pd.Series(np.exp(lcpi).round(1), index=idx, name='cpi')

def nigeria_fx(seed=817):
    s = _local('nigeria_fx', 'ngn_usd', 'MS')
    if s is not None: s.name = 'ngn_usd'; return s
    rng = np.random.default_rng(seed)
    idx = pd.date_range('2015-01-01', '2026-06-01', freq='MS'); n = len(idx)
    lv = np.log(197.0) * np.ones(n); drift = np.where(idx < '2023-06-01', 0.004, 0.012)
    steps = {'2016-06-01': np.log(283 / 197), '2020-03-01': np.log(361 / 306), '2021-05-01': np.log(410 / 379), '2023-06-01': np.log(770 / 465), '2024-01-01': np.log(1400 / 900)}
    eps = rng.normal(0, 0.012, n)
    for t in range(1, n): lv[t] = lv[t - 1] + drift[t] + eps[t] + steps.get(str(idx[t].date()), 0.0)
    return pd.Series(np.exp(lv).round(2), index=idx, name='ngn_usd')

def nigeria_grid(seed=818):
    s = _local('nigeria_grid', 'generation_mw', 'MS')
    if s is not None: s.name = 'generation_mw'; return s
    rng = np.random.default_rng(seed)
    idx = pd.date_range('2015-01-01', '2026-06-01', freq='MS'); n = len(idx)
    trend = 3500 + 9 * np.arange(n); season = 260 * np.sin(2 * np.pi * (idx.month - 4) / 12)
    e = np.zeros(n)
    for t in range(1, n): e[t] = 0.6 * e[t - 1] + rng.normal(0, 110)
    collapses = rng.choice(n, 6, replace=False); e[collapses] -= rng.uniform(250, 500, 6)
    return pd.Series((trend + season + e).round(0), index=idx, name='generation_mw')

def nigeria_malaria(seed=819):
    s = _local('nigeria_malaria', 'cases', 'W-SUN')
    if s is not None: s.name = 'cases'; return s
    rng = np.random.default_rng(seed)
    idx = pd.date_range('2019-01-06', periods=391, freq='W-SUN'); doy = idx.dayofyear.values
    mu = 900 * np.exp(0.55 * np.sin(2 * np.pi * (doy - 120) / 365.25)) * (1 + 0.02 * np.arange(len(idx)) / 52)
    mu[(idx >= '2022-08-01') & (idx < '2022-10-15')] *= 1.8
    return pd.Series(rng.negative_binomial(n=25, p=25 / (25 + mu)), index=idx, name='cases')

def nigeria_rainfall(seed=820):
    s = _local('nigeria_rainfall', 'rain_mm', 'MS')
    if s is not None: s.name = 'rain_mm'; return s
    rng = np.random.default_rng(seed)
    idx = pd.date_range('2019-01-01', '2026-06-01', freq='MS')
    mu = 30 + 230 * np.clip(np.sin(2 * np.pi * (idx.month - 3.5) / 12), 0, None) ** 1.5
    return pd.Series((mu * rng.lognormal(0, 0.25, len(idx))).round(0), index=idx, name='rain_mm')

def nigeria_covid():
    """Nigeria weekly confirmed COVID-19 cases (WHO), real snapshot only - no simulation fallback."""
    s = _local('nigeria_covid', 'cases', 'W-SUN')
    if s is None:
        raise FileNotFoundError('data/nigeria_covid.csv not found - this real series has no simulated fallback')
    s.name = 'cases'; return s

def nigeria_rain_obs():
    """Observed monthly rainfall, NASA POWER regional mean (mm), real snapshot only - no simulation fallback."""
    s = _local('nigeria_rain_obs', 'rain_mm', 'MS')
    if s is None:
        raise FileNotFoundError('data/nigeria_rain_obs.csv not found - this real series has no simulated fallback')
    s.name = 'rain_mm'; return s

def bonny_light(seed=821):
    s = _local('bonny_light', 'bonny_light', 'MS')
    if s is not None: s.name = 'bonny_light'; return s
    rng = np.random.default_rng(seed)
    idx = pd.date_range('2015-01-01', '2026-06-01', freq='MS'); n = len(idx)
    anchors = {'2015-01-01': 50, '2016-01-01': 32, '2018-10-01': 80, '2020-04-01': 20, '2022-06-01': 120, '2023-06-01': 75, '2025-01-01': 78, '2026-06-01': 70}
    a = pd.Series(anchors); a.index = pd.to_datetime(a.index)
    path = np.log(a.reindex(idx).interpolate(method='linear').values); noise = np.zeros(n)
    for t in range(1, n): noise[t] = 0.5 * noise[t - 1] + rng.normal(0, 0.05)
    return pd.Series(np.exp(path + noise).round(2), index=idx, name='bonny_light')

def daily_demand(seed=822):
    s = _local('daily_demand', 'demand_gwh', 'D')
    if s is not None: s.name = 'demand_gwh'; return s
    rng = np.random.default_rng(seed)
    idx = pd.date_range('2022-01-01', '2025-12-31', freq='D'); n = len(idx)
    base = 100 + 0.01 * np.arange(n); annual = 12 * np.cos(2 * np.pi * (idx.dayofyear - 200) / 365.25)
    weekly = np.where(idx.dayofweek >= 5, -9, 0) + np.where(idx.dayofweek == 0, -1.5, 0)
    hol = np.zeros(n)
    for y in range(2022, 2026):
        for md in ['01-01', '05-01', '06-12', '10-01', '12-25', '12-26']:
            d = pd.Timestamp(f'{y}-{md}')
            if d in idx: hol[idx.get_loc(d)] = -10
    e = np.zeros(n)
    for t in range(1, n): e[t] = 0.5 * e[t - 1] + rng.normal(0, 2.2)
    return pd.Series((base + annual + weekly + hol + e).round(2), index=idx, name='demand_gwh')
