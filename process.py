
import pandas as pd

import requests

import datetime
import time

# from params import apps


def load_params():

    # load csv
    params_df = pd.read_csv("params.csv")

    # strip columns names
    params_df.rename(columns=lambda x: x.strip(), inplace=True)

    # get string columns
    str_cols = set(params_df.dtypes[params_df.dtypes == "object"].index)
    other_cols = list(set(params_df.columns) - str_cols)

    # strip column content
    str_params_df = params_df[str_cols].apply(lambda x: x.str.strip(), axis=1)
    params_df = pd.concat([str_params_df, params_df[other_cols]], axis=1)

    # select latest batch
    latest_batch = max(params_df.batch)
    params_df = params_df[params_df.batch == latest_batch]

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
        name = app["name"]

        # ping app
        if type in ["api", "web"] and name in ["prod"]:

            log = app.copy()
            start = time.time()
            log["time"] = datetime.datetime.now()
            log["code"] = ping_app(url)

            end = time.time()
            log["duration"] = end - start

            logs.append(log)

    # save logs
    now = datetime.datetime.now()
    file_timestamp = now.strftime("%Y-%m-%d_%H-%M-%S")
    df = pd.DataFrame(logs)
    df.to_csv(f"data/{file_timestamp}_logs.csv", index=False)


def sleep():

    # for each minute
    for i in range(5):

        # new line
        print("\n", end="", flush=True)

        # for each span of 10 seconds
        for i in range(6):

            # print dot
            print(".", end="", flush=True)

            # sleep
            time.sleep(10)

    print("\n", flush=True)


def ping_all():

    params = load_params()
    ping_apps(params)
    # ping_apps(apps)


if __name__ == '__main__':
    while True:

        # ping all
        ping_all()

        # sleep
        sleep()
