
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
    for test, file in enumerate(files):

        log_df = pd.read_csv(file)
        log_df["test"] = test
        log_df["index_test"] = test
        logs_df.append(log_df)

    all = pd.concat(logs_df, axis=0)

    all["app_id"] = all.apply(lambda x: f"{x.team} {x['name']} {x.type}", axis=1)

    all.set_index("index_test", inplace=True)

    return all


def stats(df, team, prod, type, graph, package, period, offset, window):

    # filter offset and window
    min = offset
    max = offset+window-1
    df = df.loc[min:max]

    # filter team
    if team != "all":
        df = df[df.team == team]

    # filter prod
    if prod != "all":
        df = df[df.name == prod]

    # filter type
    if type != "all":
        df = df[df.type == type]

    # retrieve duration per app
    apps = df.app_id.unique()

    df["duration"] = df.duration

    df.sort_values(["time"], inplace=True)

    if graph == "data":

        "# data"

        df

    else:

        "# responses"

        if package == "altair":

            import altair as alt

            if period == "test":
                x_value = alt.X(period, scale=alt.Scale(domain=[min, max]))
            else:
                x_value = period

            c = alt.Chart(df).mark_circle().encode(
                x=x_value,
                y=alt.Y(graph, scale=alt.Scale(type="log")),
                size="code",
                color="app_id",
                tooltip=[period, "time", graph, "code", "app_id"]
            ).properties(
                width=700,
                height=500)

            st.write(c)

        elif package == "mpl_scatter":

            fig, ax = plt.subplots()
            ax.set_yscale("log")

            sns.scatterplot(data=df, x=period, y=graph, hue="app_id", size="code", ax=ax)
            st.pyplot(fig)

        elif package == "mpl_plot":

            fig, ax = plt.subplots()
            ax.set_yscale("log")

            for app in apps:

                plot_df = df[df.app_id == app][[graph]].reset_index().drop("index_test", axis=1)

                ax.plot(plot_df)

            ax.legend(apps)
            st.pyplot(fig)


# read logs
all_df = read_logs()

st.sidebar.markdown("# filters")

# list teams
teams = list(all_df.team.unique())
team = st.sidebar.radio(
    "team",
    ["all"] + teams,
    format_func=lambda x: dict(
        all="All",
        galaxy="Galaxy Finder ⭐️",
        mood="Speech Emotion Recognition 🎙",
        facemask="Face Mask Detection 😷",
        gameone="Game Book 🎲",
        bling="Bling Back The Cash 💵",
        coin="Bitcoin Prediction 💰",
        openff="Open Food Facts 🥙")[x])

# list prod
prods = list(all_df.name.unique())
prod = st.sidebar.radio(
    "prod",
    ["all"] + prods,
    format_func=lambda x: dict(
        all="All",
        prod="Prod 🤖",
        team="Team 🎨",
        alice="Alice 🐹")[x])

# list types
types = list(all_df.type.unique())
type = st.sidebar.radio(
    "type",
    ["all"] + types,
    format_func=lambda x: dict(
        all="All",
        api="API 🤖",
        web="Web 🕸",
        pres="Pres 🎨",
        repo="Repo 🐍",
        org="Project 🧮",
        status="Org 📈")[x])

cols = st.beta_columns(3)

# graph
graph = cols[0].radio(
    "graph",
    options=["duration", "code", "data"],
    format_func=lambda x: dict(
        data="Data 🧾",
        duration="Duration ⏳",
        code="Code 🚦")[x])

# period
period = ""
if graph != "data":

    period = cols[1].radio(
        "period",
        options=["test", "time"],
        format_func=lambda x: dict(
            test="Test 🤖",
            time="Time ⏰")[x])

# package
package = ""
if graph != "data":

    package = cols[2].radio(
        "viz",
        options=["altair", "mpl_scatter", "mpl_plot"],
        format_func=lambda x: dict(
            altair="Altair 🔥",
            mpl_scatter="Matplotlib Scatter ❄️",
            mpl_plot="Matplotlib Plot 📈")[x])

# offset
window = 50
max_offset = len(all_df.test.unique()) - window
offset = st.slider("offset", 0, max_offset, max_offset)

# show stats
stats(all_df, team, prod, type, graph, package, period, offset, window)
