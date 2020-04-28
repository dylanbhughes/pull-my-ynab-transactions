from prefect import task, Flow
from prefect.schedules import CronSchedule
from prefect.tasks.secrets import Secret
import requests
from datetime import timedelta


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


schedule = CronSchedule(cron="0 * * * *")

with Flow(name="Ping YNAB", schedule=schedule) as flow:
    API_KEY = Secret("YNAB_API_KEY")
    result = ping_ynab_to_import_transactions(api_key=API_KEY)
