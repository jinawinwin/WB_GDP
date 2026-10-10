# World Bank GDP Growth Monitor

A lightweight GitHub Pages dashboard for annual GDP growth and long-run real GDP growth rates using the World Bank Indicators API v2.

## Features
- Country-cluster tabs with context notes
- Annual real GDP growth (`NY.GDP.MKTP.KD.ZG`)
- Long-run CAGR (5/10/15/20/25/30 years), calculated from real GDP levels (`NY.GDP.MKTP.KD`)
- CSV export and browser print-to-PDF
- GitHub Actions data refresh on the 15th of odd-numbered months at 00:00 UTC (09:00 KST)
- Manual refresh workflow via **Actions → Update World Bank GDP data → Run workflow**

## Deploy on GitHub Pages
1. Push the project files to the repository's `main` branch.
2. Open **Settings → Pages**.
3. Set **Build and deployment → Deploy from a branch**, branch `main`, folder `/ (root)`.
4. Wait for the Pages deployment to complete.

## Data notes
- World Bank API v2 requires no API key.
- GDP growth is an annual percentage series. It is not forecast data.
- CAGR is calculated from real GDP levels, not by compounding annual growth percentages directly.
- National accounts data can be revised. Record retrieval dates when using snapshots for research.
- Forecasts should be stored separately with institution, forecast year, release/vintage date, value, and source URL. Official sources:
  - IMF WEO: https://www.imf.org/en/Publications/WEO
  - World Bank Global Economic Prospects: https://www.worldbank.org/en/publication/global-economic-prospects
  - OECD Economic Outlook: https://www.oecd.org/en/publications/oecd-economic-outlook_16097408.html

## Update schedule
`0 0 15 1,3,5,7,9,11 *` = January, March, May, July, September, November 15 at 00:00 UTC / 09:00 KST.
GitHub Actions cron is UTC and may start a little later during busy periods.
