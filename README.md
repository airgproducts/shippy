# Development
1. Install [Poetry](https://python-poetry.org/) for dependency management
2. `poetry install`
3. From now on use `poetry run myfile.py` or simply `poetry shell` to run python scripts
4. Install pre-commit hooks with `poetry run pre-commit install`

# Testing

create a .env file with your credentials to test
`poetry run pytest`

# Usage
TODO

# known issues
FAILED tests/gls/test_rates.py::test_rate_shipment - shippy.base.errors.ShippyAPIError: GLS get estimated delivery days failed with 404: {'Date': 'Mon, 08 Jul 2024 14:32:53 GMT', 'Content-Length': '0', 'Connection': 'keep-alive', 'serverExecutionTime': '0'}


# Resources
### GLS
- German GLS Developer Portal: https://www.gls-versand.com
- GLS ShipIT Documentation: https://shipit.gls-group.eu/documentation/

### UPS
- https://www.ups.com/upsdeveloperkit?loc=de_AT
