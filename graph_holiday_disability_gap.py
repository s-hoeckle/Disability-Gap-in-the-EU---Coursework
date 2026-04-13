import matplotlib.pyplot as plt
import numpy as np
import config


def plot(df):
    mask = (
        (df["age"] == "16 and over")
        & (df["sex"] == "Total")
        & (df["lev_limit"].isin(["Some or severe limitation", "No limitation"]))
        & (df["geo"].str.len() == 2)
    )
    df_filtered = df[mask].copy()

    df_pivot = df_filtered.pivot(index="geo", columns="lev_limit", values="holiday_rate_%")

    df_pivot["diff_gap"] = df_pivot["Some or severe limitation"] - df_pivot["No limitation"]
    df_pivot = df_pivot.sort_values("diff_gap", ascending=True).dropna(subset=["diff_gap"])

    y = np.arange(len(df_pivot))
    h = config.PLOT_SETTINGS["bar_height_gap"]

    plt.figure(figsize=config.PLOT_SETTINGS["figsize"])

    plt.barh(
        y - h / 2,
        df_pivot["No limitation"],
        height=h,
        label="No limitation",
        color=config.TEAL_PALETTE["teal_1"],
    )

    plt.barh(
        y + h / 2,
        df_pivot["Some or severe limitation"],
        height=h,
        label="Some or severe limitation",
        color=config.TEAL_PALETTE["teal_4"],
    )

    for i, (idx, row) in enumerate(df_pivot.iterrows()):
        gap = row["diff_gap"]
        if not np.isnan(gap):
            plt.text(
                row["Some or severe limitation"] + 0.5,
                i + h / 2,
                f"+{gap:.1f} pp",
                va="center",
                fontsize=9,
                color=config.COLORS["GAP_TEXT"],
            )

    plt.yticks(y, df_pivot.index)
    plt.xlabel("Unable to afford one week annual holiday away from home (%)")
    plt.title(
        "Disability Gap: Inability to afford one week annual holiday away from home (2021)\n(Some/Severe limitations vs No limitations, age 16+, total)"
    )
    plt.legend()
    plt.tight_layout()
