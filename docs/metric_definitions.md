# Metric Definitions

Written in plain language BEFORE any code is generated (required by the brief).

| Metric | Plain-language definition | How it's worked out | How to read it | Why it matters for the business question | Inputs | Window |
|---|---|---|---|---|---|---|
| 20-day rolling average | It is the average closing level of the ASX 200 over the most recent 20 days of trading. It is recalculated every single day | Every day, you add up that day's close and the 19 days before it, then divide the value by 20. The first 19 days have no values as there is not enough history yet | If today's close is above the line, then the market is doing better than it's recent standard. If it is below, then the market close is doing worse | Daily prices are always moving up and down. This line clears away the noise and makes it easier for a non-technical reader to see the underlying direction and whether today looks unusual | asx200_close | 20 trading days |
| 14-day volatility |It is a measure of how much the ASX 200's daily moves have been fluctuating over the last 14 trading days | The percentage change of each days close is calculated, then measure how spread out the last 14 days of those changes are (standard deviation). It is shows as % per day | A low number means the market has been moving steadily while a high number means bigger fluctuations up and down | It answers the question "Is there anything we should be watching?", because a jump in volatility means that market conditions are less predictable, even when the price hasn't moved much | asx200_close (via daily % change) | 14 trading days |
| 30-day rolling correlation | | Green if it’s below the middle (50th percentile) of the past year’s readings, Amber if it’s between the 50th and 80th percentile, and Red if it’s above the 80th. ||| sp500_close, vix_close | 30 trading days |

Written by: Abdul Rahman Farzan Rizvi
Date: 26/10/2026
