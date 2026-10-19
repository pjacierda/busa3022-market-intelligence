# busa3022-market-intelligence
# Really Big Bank – Market Intelligence Analytics
BUSA3022 Analytics Lead Case Study (Group)

## Goal
Show how market activity has trended over the past 90 days and flag anything worth watching.

## Data sources
- Market index: S&P 500 (^GSPC) – Yahoo Finance, daily
- Macro series: VIX (VIXCLS) – FRED, daily

## Data contract (data/clean/market_daily.csv)
| Column | Meaning |
|---|---|
| date | US/Eastern trading date (YYYY-MM-DD) |
| sp500_close | S&P 500 closing price |
| sp500_volume | S&P 500 daily volume |
| vix_close | VIX close (forward-filled where missing) |
| vix_missing | True if VIX value was filled |

## Team
- Pipeline lead: 
- Curation lead: 
- Dashboard lead: 
- Integrator / presentation lead: 

## Rules
- Never commit API keys – use Colab Secrets
- Don't change the data contract without group agreement
- Log any AI mistakes in docs/ai_log.md
