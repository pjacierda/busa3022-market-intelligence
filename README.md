# Really Big Bank – Market Intelligence Analytics
BUSA3022 Analytics Lead Case Study (Group)

## Goal
Show how the Australian share market has trended over the past 90 days and flag anything worth watching.

## Data sources
- Market index: S&P/ASX 200 (^AXJO) – Yahoo Finance, daily
- Macro series: Australian Government 10-year bond yield (FCMYGBAG10D) – RBA table F2, daily

## Data contract (data/clean/market_daily.csv)
| Column | Meaning |
|---|---|
| date | Sydney trading date (YYYY-MM-DD) |
| asx200_close | ASX 200 closing level |
| asx200_volume | ASX 200 daily volume |
| bond10y_yield | 10-year bond yield, % (forward-filled where missing) |
| bond10y_missing | True if the yield was filled rather than published |

## Load the data
```python
import pandas as pd
df = pd.read_csv("https://raw.githubusercontent.com/pjacierda/busa3022-market-intelligence/main/data/clean/market_daily.csv")
```

## Team
- Pipeline lead: Pierce
- Curation lead: 
- Dashboard lead: 
- Integrator / presentation lead: 

## Rules
- Never commit API keys – use Colab Secrets
- Don't change the data contract without group agreement
- Log any AI mistakes in docs/ai_log.md
