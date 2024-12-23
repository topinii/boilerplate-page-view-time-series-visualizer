import numpy as np
np.float = float

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Load and clean the data
df = pd.read_csv("fcc-forum-pageviews.csv", index_col="date", parse_dates=True)

# Filter data for 2.5th and 97.5th percentiles
lower_limit = df["value"].quantile(0.025)
upper_limit = df["value"].quantile(0.975)
df = df[(df["value"] >= lower_limit) & (df["value"] <= upper_limit)]


def draw_line_plot():
    # Draw the line plot
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df.index, df["value"], color="red", linewidth=1)
    ax.set_title("Daily freeCodeCamp Forum Page Views 5/2016-12/2019")
    ax.set_xlabel("Date")
    ax.set_ylabel("Page Views")

    # Save image and return
    fig.savefig("line_plot.png")
    return fig


def draw_bar_plot():
    # Prepare data for bar plot
    df_bar = df.copy()
    df_bar["year"] = df.index.year
    df_bar["month"] = df.index.month_name()

    # Order months from January to December
    month_order = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    df_bar["month"] = pd.Categorical(df_bar["month"], categories=month_order, ordered=True)

    # Group by year and month
    df_bar = df_bar.groupby(["year", "month"])["value"].mean().unstack()

    # Draw bar plot
    fig = df_bar.plot(kind="bar", figsize=(12, 6), legend=True).figure
    plt.title("Average Daily Page Views per Month")
    plt.xlabel("Years")
    plt.ylabel("Average Page Views")
    plt.legend(title="Months")

    # Save image and return
    fig.savefig("bar_plot.png")
    return fig


def draw_box_plot():
    # Prepare data for box plots
    df_box = df.copy()
    df_box["year"] = df.index.year
    df_box["month"] = df.index.month_name()
    df_box["month_num"] = df.index.month
    df_box.sort_values("month_num", inplace=True)

    # Abbreviate month names for the second box plot (Month-wise Box Plot)
    month_abbr = {
        "January": "Jan", "February": "Feb", "March": "Mar", "April": "Apr", "May": "May",
        "June": "Jun", "July": "Jul", "August": "Aug", "September": "Sep", "October": "Oct",
        "November": "Nov", "December": "Dec"
    }
    df_box["month_abbr"] = df_box["month"].map(month_abbr)

    # Draw box plots
    fig, axes = plt.subplots(1, 2, figsize=(15, 6), sharey=True)
    sns.boxplot(x="year", y="value", data=df_box, ax=axes[0])
    sns.boxplot(x="month_abbr", y="value", data=df_box, ax=axes[1])

    # Set titles and labels
    axes[0].set_title("Year-wise Box Plot (Trend)")
    axes[0].set_xlabel("Year")
    axes[0].set_ylabel("Page Views")

    axes[1].set_title("Month-wise Box Plot (Seasonality)")
    axes[1].set_xlabel("Month")
    axes[1].set_ylabel("Page Views")

    # Save image and return
    fig.savefig("box_plot.png")
    return fig
