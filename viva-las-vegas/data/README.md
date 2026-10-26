# Input data

Licensed and third-party price data are not in this repo. Put the files below in this folder
(or point `P10_DATA` at your Sharadar copy for the stock-level articles) and the code runs unchanged.

| file | source |
|---|---|
| `jkp_usa_factors_monthly.csv` | Jensen, Kelly & Pedersen factor data (jkpfactors.com): download the USA/World factor returns. |

`french_us_5f_daily.csv`, `french_us_mom_daily.csv`: Fama–French five factors and momentum, daily, from Kenneth French's data library (public). Used by `code/reported_factor.py` (section 4).
