
import pandas as pd

import os
import sys
import requests
# import traceback

import datetime
import time


def load_params(req_batch=None):

    # load csv
    params_df = pd.read_csv("params.csv")

    # filter batches
    if req_batch is not None:
        params_df = params_df[params_df.batch == req_batch]

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

    return params_list, latest_batch


def ping_app(url):

    # ping site
    print(f"ping {url}")
    try:
        response = requests.get(url)
    except Exception as e:
        print(f"\nping {url} 🚨 exception:\n{e}\n")
        # print(traceback.format_exc())
        return -1

    # return status code
    return response.status_code


def ping_apps(app_list, batch):

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
    file_path = os.path.join(
        os.path.dirname(__file__),
        "data",
        str(batch),
        f"{file_timestamp}_logs.csv")
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    df.to_csv(file_path, index=False)


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


def ping_all(req_batch=None):

    params, batch = load_params(req_batch)
    ping_apps(params, batch)


if __name__ == '__main__':

    # retrieve batch from cli params
    batch = None if len(sys.argv) < 2 else sys.argv[1]

    # convert param
    try:
        if batch is not None:
            batch = int(batch)
    except ValueError:
        batch = None

    while True:

        # ping all
        ping_all(batch)

        # sleep
        sleep()
