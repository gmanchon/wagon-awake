
import pandas as pd

import requests

import datetime

from params import apps


def ping_app(url):

    # ping site
    print(f"ping {url}")
    response = requests.get(url)

    # return status code
    return response.status_code


def ping_apps():

    # iterate through apps
    logs = []

    for app in apps:

        type = app["type"]
        url = app["url"]

        # ping app
        if type in ["api", "web"]:

            log = app.copy()
            log["code"] = ping_app(url)
            log["time"] = datetime.datetime.now()

            logs.append(log)

    # save logs
    now = datetime.datetime.now()
    file_timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    df = pd.DataFrame(logs)
    df.to_csv(f"data/{file_timestamp}_logs.csv")


if __name__ == '__main__':
    ping_apps()
