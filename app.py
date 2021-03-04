
import streamlit as st

import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns

import glob
import os


def read_logs():

    # list files sorted by time
    files = glob.glob(os.path.join("data", "*.csv"))
    files.sort(key=os.path.getmtime)

    # iterate through log files
    logs_df = []
    for index, file in enumerate(files):

        log_df = pd.read_csv(file)
        log_df["index"] = index
        logs_df.append(log_df)

    all = pd.concat(logs_df, axis=0)

    all["app_id"] = all.apply(lambda x: f"{x.team} {x['name']} {x.type}", axis=1)

    return all


def stats(df):

    # retrieve duration per app
    apps = df.app_id.unique()

    df["duration"] = df.duration

    df.sort_values(["time"], inplace=True)

    df

    "# responses"

    fig, ax = plt.subplots()

    sns.scatterplot(data=df, x="index", y="duration", hue="app_id", size="code", ax=ax)
    st.pyplot(fig)

    "# duration"

    fig, ax = plt.subplots()

    for app in apps:

        duration = df[df.app_id == app][["duration"]].reset_index().drop("index", axis=1)

        ax.plot(duration)

    ax.legend(apps)
    st.pyplot(fig)

    "# status code"

    fig, ax = plt.subplots()

    for app in apps:

        code = df[df.app_id == app][["code"]].reset_index().drop("index", axis=1)

        ax.plot(code)

    ax.legend(apps)
    st.pyplot(fig)


if __name__ == '__main__':
    res = read_logs()
    print(res)
    stats(res)
