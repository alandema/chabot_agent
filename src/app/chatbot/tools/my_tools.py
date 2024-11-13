import requests
import json
from langchain_core.tools import tool


@tool(parse_docstring=True)
def get_currency(output_currency: str, amount: float, date: str) -> float:
    """This API converts an amount of euros to another currency on a specific date.

    Args:
        output_currency: Desired currency using ISO 4217 as string
        amount: Amount of euros as float
        date: Date in format YYYY-MM-DD as string
    """
    url = "https://api.frankfurter.app/" + date
    response = requests.get(url)
    r_json = response.json()
    return r_json["rates"][output_currency] * amount


if __name__ == "__main__":
    # print(get_currency("USD", 100, "2024-09-25"))
    print(get_currency.name)
    print(get_currency.args)
    print(get_currency.description)
