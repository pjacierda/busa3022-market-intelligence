# AI Agent Log

Record every time an AI tool gave wrong or incomplete output. These examples are required for the AI reflection.

| Date | Who | Tool | What we asked | What went wrong | How we caught it | Fix |
|---|---|---|---|---|---|---|
 2026-10-21 | Pierce | Claude (Anthropic) | Generate a starter pipeline to ingest S&P 500 (Yahoo) and VIX (FRED), validate, and merge on date | Notebook assumed missing VIX values were mostly US holidays. On the first live run, the only gap in the merged data was 20 Oct 2026, a normal trading day, because FRED had not yet published that day's value (publication delay, not a holiday) | Checked the forward-fill log against the date in the clean output and saw 20 Oct was a weekday when the S&P traded | Handling (forward-fill + vix_missing flag) still correct; update notebook explanation and consider only using data up to the previous trading day |
| 2026-10-21 | Pierce | Claude (Anthropic) | Starter pipeline ingestion of S&P 500 from Yahoo Finance | Notebook kept the latest trading day without checking whether its figures were final. 20 Oct 2026 volume was ~2.7B vs a usual 4–6B, likely provisional when pulled soon after the US close | Compared the latest day's volume with the previous 10 days in the clean output and saw it was roughly half the normal level | Added a rule to exclude the latest day when the run happens on the same US/Eastern date, logged as a WARN |
