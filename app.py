
import streamlit as st

import pandas as pd

import matplotlib.pyplot as plt

import glob
import os


def read_logs():

    # iterate through log files
    logs_df = []
    for file in glob.iglob(os.path.join("data", "*.csv")):

        log_df = pd.read_csv(file)
        logs_df.append(log_df)

    all = pd.concat(logs_df, axis=0)

    all["app_id"] = all.apply(lambda x: f"{x.team} {x['name']} {x.type}", axis=1)

    return all


def stats(df):

    # retrieve duration per app
    apps = df.app_id.unique()

    df["duration"] = df.duration / 1_000

    df.sort_values("time", inplace=True)

    # show app duration
    for app in apps:

        st.write(f"# {app}")

        duration = df[df.app_id == app][["duration"]].reset_index().drop("index", axis=1)

        fig, ax = plt.subplots()
        ax.plot(duration)
        st.pyplot(fig)


if __name__ == '__main__':
    res = read_logs()
    print(res)
    stats(res)
