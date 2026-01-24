import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import config
import util


def plot(gbv_df, edu_df):
    v_gap = util.get_violence_gap(gbv_df)
    e_gap = util.get_broad_education_gap(edu_df)

    df = pd.concat([v_gap, e_gap], axis=1, join="inner").dropna()
    df = util.remove_outliers(df, columns=["violence_gap", "broad_edu_gap"], threshold=3.0)

    plt.figure(figsize=(10, 8))

    plt.scatter(
        df["broad_edu_gap"],
        df["violence_gap"],
        color=config.TEAL_PALETTE["teal_4"],
        s=100,
        alpha=0.8,
        edgecolors="white",
        zorder=2,
    )

    for country, row in df.iterrows():
        plt.text(
            row["broad_edu_gap"] + 0.2,
            row["violence_gap"] + 0.2,
            country,
            fontsize=9,
            color=config.TEAL_PALETTE["teal_6"],
        )

    if len(df) > 1:
        z = np.polyfit(df["broad_edu_gap"], df["violence_gap"], 1)
        p = np.poly1d(z)

        x_range = np.linspace(df["broad_edu_gap"].min(), df["broad_edu_gap"].max(), 100)
        plt.plot(
            x_range,
            p(x_range),
            color=config.TEAL_PALETTE["teal_2"],
            linestyle="--",
            linewidth=2,
            label="Trend Line",
            zorder=1,
        )

        corr = df["broad_edu_gap"].corr(df["violence_gap"])
        plt.legend([f"Trend (r = {corr:.2f})"])

    plt.title(
        "Correlation: Education Gap (Broad - ISCED above 3) vs. Violence Gap"
    )
    plt.xlabel(
        "Education Gap (pp)\n(Inequality in attaining at least Upper Secondary education)"
    )
    plt.ylabel("Violence Risk Gap (pp)\n(Excess reports of violence by disabled women)")

    plt.grid(True, linestyle="--", alpha=0.3, color="gray")
    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["right"].set_visible(False)

    plt.tight_layout()
