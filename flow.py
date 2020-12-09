from datetime import timedelta

from prefect import task, Flow
from prefect.tasks.secrets import PrefectSecret

import requests


@task(
    name="Ping YNAB to Import Transactions",
    max_retries=10,
    retry_delay=timedelta(seconds=30),
)
def ping_ynab_to_import_transactions(api_key):
    response = requests.post(
        url="https://api.youneedabudget.com/v1/budgets/last-used/transactions/import",
        headers={"Authorization": f"Bearer {api_key}"},
    )
    print(response)
    return response


with Flow(name="Ping YNAB") as flow:
    API_KEY = PrefectSecret("YNAB_API_KEY")
    result = ping_ynab_to_import_transactions(api_key=API_KEY)
