# AI Agent Log

Record every time an AI tool gave wrong or incomplete output. These examples are required for the AI reflection.

| Date | Who | Tool | What we asked | What went wrong | How we caught it | Fix |
|---|---|---|---|---|---|---|
 2026-10-21 | Pierce | Claude (Anthropic) | Generate a starter pipeline to ingest S&P 500 (Yahoo) and VIX (FRED), validate, and merge on date | Notebook assumed missing VIX values were mostly US holidays. On the first live run, the only gap in the merged data was 20 Oct 2026, a normal trading day, because FRED had not yet published that day's value (publication delay, not a holiday) | Checked the forward-fill log against the date in the clean output and saw 20 Oct was a weekday when the S&P traded | Handling (forward-fill + vix_missing flag) still correct; update notebook explanation and consider only using data up to the previous trading day |
