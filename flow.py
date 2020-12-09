from datetime import timedelta

from prefect import task, Flow
from prefect.tasks.secrets import PrefectSecret
from prefect.environments.storage import GitHub
from prefect.run_configs import KubernetesRun

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
    path="flow.py",
    secrets=["YNAB_GITHUB_ACCESS_TOKEN"],
)

with Flow(name="Pull My YNAB Transactions", storage=storage) as flow:
    API_KEY = PrefectSecret("YNAB_API_KEY")
    result = ping_ynab_to_import_transactions(api_key=API_KEY)

flow.run_config = KubernetesRun(
    image="prefecthq/prefect:all_extras", cpu_request=1, memory_request="2Gi"
)
