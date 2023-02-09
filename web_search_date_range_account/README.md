# Web Search Date Range Account

This module extends the web_search_date_range module with date ranges related to accounting.

It enables date filters that are bound to the fiscal year of the company.

For now, the following filters are available.

* Previous Trimester
* Current Trimester
* Next Trimester
* Previous Fiscal Year
* Current Fiscal Year
* Next Fiscal Year

## Adding Date Filters

To add a filter to the search view of a model:

* Go to: Settings / Technical / User Interface / Date Filters

![Date Filters](static/description/date_filters.png?raw=true)

* Go to the list view of the model (i.e. Journal Items)

![Account Move Lines](static/description/account_move_lines.png?raw=true)

## How the module works

The module uses the Fiscal Year settings to determine the fiscal year and trimester ranges.

![Fiscal Year Last Day](static/description/fiscal_year_last_day.png?raw=true)

## Multi-Company

The module works with multi-company.

If you have subsidiaries with different account closing dates, the same filters will work for all.
You will not need to recreate your dashboards for each subsidiary.

Contributors
------------
* Numigi (tm) and all its contributors (https://bit.ly/numigiens)
