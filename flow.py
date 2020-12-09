from datetime import timedelta

from prefect import task, Flow
from prefect.tasks.secrets import PrefectSecret
from prefect.environments.storage import GitHub

import requests


@task(
    name="Ping YNAB to Import Transactions",
    max_retries=10,
    retry_delay=timedelta(seconds=30),
    log_stdout=True,
)
def ping_ynab_to_import_transactions(api_key):
    response = requests.post(
        url="https://api.youneedabudget.com/v1/budgets/last-used/transactions/import",
        headers={"Authorization": f"Bearer {api_key}"},
    )
    print(response)
    return response


storage = GitHub(
    repo="dylanbhughes/pull-my-ynab-transactions",
    path="my_flow.py",
    secrets=["YNAB_GITHUB_ACCESS_TOKEN"],
)

with Flow(name="Ping YNAB", storage=storage) as flow:
    API_KEY = PrefectSecret("YNAB_API_KEY")
    result = ping_ynab_to_import_transactions(api_key=API_KEY)
