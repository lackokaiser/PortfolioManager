# PortfolioManager

A course project designed to browse a portfolio.

The application is designed based on the following requirements:
* Browse a portfolio
* View the performance of the portfolio (ideally in some graphical manner)
* Add items to the portfolio
* Remove items from the portfolio

## Functional requirements
You will need to run your own MySQL instance provided by the instructor team. Ideally, you should run this from the provided VM. For now the SQL access is hardcoded in the project, you should change it in case you are using a different MySQL instance.

## Architecture
There are two wrappers in the project: One for SQL access and one for Yahoo Finance.

The aim was to have SQL and Yahoo Finance related code in their separate module. This will make maintenance easier, as if there is a problem with SQL, we only need to check and update one location instead of finding every SQL usage in the codebase.

Flask calls these wrappers to receive the information needed by the client and returns it in a json format.

The client will call these endpoints and process the information received. This approach makes the client very flexible, as it is no longer dependent on Flask itself, allowing the use of other technologies to write it.
