import matplotlib.pyplot as plt
import numpy as np
import config


def plot(df):
    mask = (
        (df["age"] == "Y_GE16")
        & (df["sex"] == "T")
        & (df["lev_limit"].isin(["SM_SEV", "NONE"]))
        & (df["geo"].str.len() == 2)
    )
    df_filtered = df[mask].copy()

    df_pivot = df_filtered.pivot(index="geo", columns="lev_limit", values="health_rate_%")

    df_pivot["diff_gap"] = df_pivot["SM_SEV"] - df_pivot["NONE"]
    df_pivot = df_pivot.sort_values("diff_gap", ascending=True).dropna(subset=["diff_gap"])

    y = np.arange(len(df_pivot))
    h = config.PLOT_SETTINGS["bar_height_gap"]

    plt.figure(figsize=config.PLOT_SETTINGS["figsize"])

    plt.barh(
        y - h / 2,
        df_pivot["NONE"],
        height=h,
        label="No limitation (NONE)",
        color=config.TEAL_PALETTE["teal_1"],
    )

    plt.barh(
        y + h / 2,
        df_pivot["SM_SEV"],
        height=h,
        label="Some or severe limitation (SM_SEV)",
        color=config.TEAL_PALETTE["teal_4"],
    )

    for i, (idx, row) in enumerate(df_pivot.iterrows()):
        gap = row["diff_gap"]
        if not np.isnan(gap):
            plt.text(
                row["SM_SEV"] + 0.5,
                i + h / 2,
                f"+{gap:.1f} pp",
                va="center",
                fontsize=9,
                color=config.COLORS["GAP_TEXT"],
            )

    plt.yticks(y, df_pivot.index)
    plt.xlabel("Reporting good or very good health (%)")
    plt.title(
        "Health Gap: Difference in self-perceived good health (2021)\n(Some/Severe limitations vs No limitations, age 16+, total)"
    )
    plt.legend()
    plt.tight_layout()
