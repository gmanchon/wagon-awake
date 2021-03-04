
import pandas as pd

import requests

import datetime


apps = [dict(
    team="galaxy",
    name="prod",
    type="api",
    url="https://star-wars-mptzkkztqq-ew.a.run.app/",
), dict(
    team="galaxy",
    name="prod",
    type="web",
    url="https://galaxystreamlit.herokuapp.com/",
), dict(
    team="galaxy",
    name="alice",
    type="api",
    url="https://hamster-ev6iq3m3na-ew.a.run.app/",
), dict(
    team="mood",
    name="prod",
    type="pres",
    url="https://www.beautiful.ai/player/-MUrnVCdxzKexGOLpEgr/Back-in-the-SSR",
), dict(
    team="mood",
    name="prod",
    type="repo",
    url="https://github.com/Celine-Guan/backinthessr",
), dict(
    team="mood",
    name="prod",
    type="web",
    url="https://backinthessr.herokuapp.com/",
)]


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
