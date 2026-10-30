# RAG signal and threshold

**What it measures-** The signal measures 14-day volatility, showing how much the ASX 200’s daily percentage movements have varied over the last 14 trading days. Unlike the index level, which doesn't indicate market conditions, volatility helps determine if the market is stable or erratic.

**Why compare with the past year?-** Using a fixed cut-off like “red above 1% a day” is arbitrary and can misrepresent market stability over time. Instead, today’s volatility is compared to the past 252 trading days (about a year), allowing for a meaningful colour code that indicates what is unusual for this market this year (LuxAlgo, n.d.). For instance, on 27 October 2026, volatility was 0.53% per day, higher than only 24% of the past year, resulting in a green signal.

**Why use 50th and 80th percentiles?-** Our system categorises volatility as follows: Green for below the 50th percentile, Amber for 50th to 80th, and Red for above the 80th. This distribution is designed to result in about 50% Green, 30% Amber, and 20% Red. Red is reserved for extreme volatility to prompt action. Because the percentile method always produces about 50/30/20, the five biggest one-day falls in the past year were used as an independent check. We tested different thresholds: looser ones (40/70) flagged all major falls but created alert fatigue, with only 40% of days green and 30% Red. Tighter thresholds (60/90) missed significant declines. The chosen 50/80 setting flagged four out of five major drops as Amber or Red, providing a balanced approach. The sensitivity check is in dashboard/dashboard.ipynb (cell 12b).

**Limitations-** Volatility confirms changes only after they begin, so it doesn't predict market movements; it also requires a year of historical data to be effective, and the latest day’s data may be provisional. This evaluation used the last year’s thresholds across the entire period, serving as a sanity check rather than definitive proof.

## Reference

LuxAlgo. (n.d.). *Volatility percentile rank*. Retrieved 31 October 2026, from https://www.luxalgo.com/library/concept/volatility-percentile-rank/
