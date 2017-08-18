# Using Title and Body templates with the Squirro Data Loader

This example shows how Jinja2 Templates can be used to generate complex title and body contents from the data included within a squirro item.

## What is a Jinja2 Template?

Within Squirro, Jinja templates allow you to programmatically generate HTML based on the contents of a given Squirro item or row of input data.

### Template Basics

Within HTML contents, Jinja Templates will include additional elements within the following types of delimiters:

* `{% ... %}` for Statements, like `if`, `for`, `while`, etc.
* `{{ ... }}` for Expressions to print directly to the template output
* `{# ... #}` for Comments not included in the template output
* `#  ... ##` for Line Statements


```jinja
<!DOCTYPE html>
<html lang="en">
<head>
    <title>My Webpage</title>
</head>
<body>
    <ul id="navigation">
    {% for item in navigation %}
        <li><a href="{{ item.href }}">{{ item.caption }}</a></li>
    {% endfor %}
    </ul>

    <h1>My Webpage</h1>
    {{ a_variable }}

    {# a comment #}
</body>
</html>
```

For more information on Jinja Templates, see their documentation [Here](http://jinja.pocoo.org/docs/2.9/)

## Our Test Data Set
We will continue to use our test CSV data set from the previous examples.
The data set looks like this:

|id|company|ticker|ipo_date|number_employees|link|
|---|---|---|---|---|---|
|1|Apple|AAPL|1980-12-12T00:00:00|116000|https://finance.yahoo.com/quote/AAPL|
|2|Google|GOOG|2004-08-19T00:00:00|73992|https://finance.yahoo.com/quote/GOOG|
|3|Microsoft|MSFT|1986-03-13T00:00:00|120849|https://finance.yahoo.com/quote/MSFT|
|4|Amazon|AMZN|1997-05-15T00:00:00|341400|https://finance.yahoo.com/quote/AMZN|
|5|Intel|INTC|1978-01-13T00:00:00|106000|https://finance.yahoo.com/quote/INTC|

## Constructing a Load Script
To use a jinja template for the title or body of the item, add one or both of the following lines to your load script:
```bash
--title-template-file 'title.j2' \
--body-template-file 'body.j2' \
```
