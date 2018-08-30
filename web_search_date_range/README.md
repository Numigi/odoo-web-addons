# Web Search Date Range

This module adds the possibility to easily add contextual date range filters.

Contextual means that the filter does not need to be updated.
It always filters records based on the current date.

You may add one of these filters to your favorites or your dashboard and it will not need to be refreshed.

![List View](static/description/partner_list.png?raw=true)

## Date Filters

To edit the list of filters that appear in the search view of a model:

* Go to: Settings / Technical / User Interface / Date Filters

![Date Filters](static/description/date_filters.png?raw=true)

## Date Range Types

A date range type is a contextual domain filter that can be used for any date or datetime field.

Currently, the following date range types are implemented:

* Before Today
* Today
* Next Fifteen Days
* Previous Week
* Current Week
* Next Week
* Previous Month
* Current Month
* Next Month
* Previous Year
* Current Year
* Next Year

To add a custom range type:

* Go to: Settings / Technical / User Interface / Date Ranges
* Click on `Create`.
* Enter a label for your range type.
* Enter a domain filter for your new range type.

The domain you enter must contain `{field}` instead of a field name.
This allows to make the range type reusable.

Example of domain for the filter Today:
```python
[
    ('{field}', '&gt;=', context_today().strftime('%Y-%m-%d')),
    ('{field}', '&lt;', (context_today() + relativedelta(days=1)).strftime('%Y-%m-%d')),
]
```

## Weekly Date Ranges

Weekly date ranges are implemented from monday to sunday.

If you prefer from sunday to saturday:

* Go to: Settings / Technical / User Interface / Date Range Types.
* For each weekly range type:
	1. Adapt the contextual domain.
	3. Check the `No Update` checkbox.

Contributors
------------
* Numigi (tm) and all its contributors (https://bit.ly/numigiens)
