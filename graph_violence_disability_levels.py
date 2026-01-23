import matplotlib.pyplot as plt
import numpy as np
import config


def plot(df):
    df_pivot = df.pivot(index="geo", columns="lev_limit", values="abuse_rate_%")
    df_pivot = df_pivot.sort_values("NONE")

    y = np.arange(len(df_pivot)) * config.PLOT_SETTINGS["group_spacing"]
    h = config.PLOT_SETTINGS["bar_height"]

    plt.figure(figsize=config.PLOT_SETTINGS["figsize"])

    plt.barh(
        y - h,
        df_pivot["NONE"],
        height=h,
        label="No limitation in activity",
        color=config.COLORS["NONE"],
    )

    plt.barh(
        y,
        df_pivot["SOME"],
        height=h,
        label="Some limitation in activity",
        color=config.COLORS["SOME"],
    )

    plt.barh(
        y + h,
        df_pivot["SEV"],
        height=h,
        label="Severe limitation in activity",
        color=config.COLORS["SEV"],
    )

    plt.yticks(y, df_pivot.index)
    plt.xlabel("Reported violence (%)")
    plt.ylabel("Country")
    plt.title(
        "Women who have experienced violence by any partner by level of disability (2021)"
    )
    plt.legend()
    plt.tight_layout()
