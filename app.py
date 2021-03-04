
import pandas as pd

import streamlit as st

import glob
import os


def read_logs():

    # iterate through log files
    logs_df = []
    for file in glob.iglob(os.path.join("data", "*.csv")):

        log_df = pd.read_csv(file)
        logs_df.append(log_df)

    return pd.concat(logs_df, axis=0)


if __name__ == '__main__':
    res = read_logs()
    print(res)
