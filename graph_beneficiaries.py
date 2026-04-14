import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import config


def plot(df):
    df_filtered = df[df["spdepb"] == "DIS_TOT"].copy()
    df_filtered = df_filtered.dropna(subset=["beneficiaries"])
    df_filtered = df_filtered.sort_values("beneficiaries", ascending=True)

    plt.figure(figsize=config.PLOT_SETTINGS["figsize"])

    plt.barh(
        df_filtered["geo"],
        df_filtered["beneficiaries"],
        color=config.TEAL_PALETTE["teal_3"],
    )

    plt.gca().xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x/1_000_000:.1f}M"))
    plt.xlabel("Number of beneficiaries (millions of persons)")
    plt.title(
        "Total Disability Benefit Beneficiaries by Country (2023)\n(Total scheme, all disability benefit types)"
    )
    plt.tight_layout()
