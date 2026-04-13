import matplotlib.pyplot as plt
import config


def plot(df):
    df_filtered = df.copy()
    df_filtered = df_filtered.dropna(subset=["pc_gdp"])
    df_filtered = df_filtered.sort_values("pc_gdp", ascending=True)

    plt.figure(figsize=config.PLOT_SETTINGS["figsize"])

    plt.barh(
        df_filtered["geo"],
        df_filtered["pc_gdp"],
        color=config.TEAL_PALETTE["teal_3"],
    )

    plt.xlabel("Disability benefit expenditure (% of GDP)")
    plt.title(
        "Social Protection Expenditure on Disability Benefits by Country (2023)\n(Total scheme, all benefit types, % of GDP)"
    )
    plt.tight_layout()
