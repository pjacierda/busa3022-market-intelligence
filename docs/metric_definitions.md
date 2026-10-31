# Metric Definitions

Written in plain language BEFORE any code is generated (required by the brief).

Input: `data/clean/market_daily.csv`, one row per ASX trading day (Sydney date): `date, asx200_close, asx200_volume, bond10y_yield, bond10y_missing`.

| Metric | Plain-language definition | How it's worked out | How to read it | Why it matters for the business question | Inputs | Window |
|---|---|---|---|---|---|---|
| 20-day rolling average | It is the average closing level of the ASX 200 over the most recent 20 days of trading. It is recalculated every single day | Every day, you add up that day's close and the 19 days before it, then divide the value by 20. The first 19 days have no values as there is not enough history yet | If today's close is above the line, then the market is doing better than its recent standard. If it is below, then the market close is doing worse | Daily prices are always moving up and down. This line clears away the noise and makes it easier for a non-technical reader to see the underlying direction and whether today looks unusual | asx200_close | 20 trading days |
| 14-day volatility | It is a measure of how much the ASX 200's daily moves have been fluctuating over the last 14 trading days | The percentage change of each day's close is calculated, then we measure how spread out the last 14 days of those changes are (sample standard deviation). It is shown as % per day | A low number means the market has been moving steadily while a high number means bigger fluctuations up and down | It answers the question "Is there anything we should be watching?", because a jump in volatility means that market conditions are less predictable, even when the price hasn't moved much | asx200_close (via daily % change) | 14 trading days |
| 30-day rolling correlation | It measures how closely the ASX 200's daily moves and the daily changes in the 10-year bond yield have moved together over the last 30 trading days | Each day, take the ASX 200's % change and the yield's change in basis points (1 bp = 0.01 percentage points), then calculate the correlation over the last 30 trading days. A day is left out if its yield, or the day before's, was carried forward (a copied value would look like "no change"). No value if fewer than 20 real days remain; the number of days used is shown | -1 means they always move in opposite directions, 0 means no link, +1 means they always move together. Correlation describes what happened, not what caused it | It is the macro overlay: it shows whether shares and borrowing costs are moving together or apart, which management can watch alongside the bank's own performance | asx200_close, bond10y_yield, bond10y_missing | 30 trading days (at least 20 real days) |

## Rules that apply to all three metrics

- "20-day", "14-day" and "30-day" mean trading rows, not calendar days.
- Rows are sorted by date first, and duplicate dates are refused.
- Warm-up rows stay empty, never zero.
- Volume is not used in any metric. It had a zero on 29 June 2026 and runs of repeated values, so it is kept only as a data check.

## RAG signal (uses the 14-day volatility)

| Status | Rule | What the reader does |
|---|---|---|
| Green | Below the 50th percentile of the past 252 trading days | No action needed |
| Amber | Between the 50th and 80th percentile | Keep watching |
| Red | Above the 80th percentile | Review |

Written by: Abdul Rahman Farzan Rizvi
Date: 26/10/2026

Correlation row and shared rules completed by: Duy Thinh Nguyen (curation lead)
Date: 31/10/2026. The correlation row in the first draft held the RAG rule and the old S&P 500/VIX inputs by mistake.
