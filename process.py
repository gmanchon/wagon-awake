
import pandas as pd

import requests

import datetime

# from params import apps


def load_params():

    # load csv
    params_df = pd.read_csv("params.csv")

    # strip columns names
    params_df.rename(columns=lambda x: x.strip(), inplace=True)

    # strip column content
    params_df = params_df.apply(lambda x: x.str.strip(), axis=1)

    # return list of dictionaries
    params_list = [v for _, v in params_df.T.to_dict().items()]

    return params_list


def ping_app(url):

    # ping site
    print(f"ping {url}")
    response = requests.get(url)

    # return status code
    return response.status_code


def ping_apps(app_list):

    # iterate through apps
    logs = []

    for app in app_list:

        type = app["type"]
        url = app["url"]

        # ping app
        if type in ["api", "web"]:

            log = app.copy()
            start = datetime.datetime.now()
            log["time"] = start
            log["code"] = ping_app(url)

            end = datetime.datetime.now()
            log["duration"] = (end - start).microseconds

            logs.append(log)

    # save logs
    now = datetime.datetime.now()
    file_timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    df = pd.DataFrame(logs)
    df.to_csv(f"data/{file_timestamp}_logs.csv", index=False)


if __name__ == '__main__':
    params = load_params()
    ping_apps(params)
    # ping_apps(apps)
