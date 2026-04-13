import matplotlib.pyplot as plt
import config


EXCLUDED_AGGREGATES = {"EEA_X_LI", "EFTA_X_LI"}


def plot(df):
    df_filtered = df[~df["geo"].isin(EXCLUDED_AGGREGATES)].copy()
    df_filtered = df_filtered.dropna(subset=["mio_eur"])
    df_filtered = df_filtered.sort_values("mio_eur", ascending=True)

    plt.figure(figsize=config.PLOT_SETTINGS["figsize"])

    plt.barh(
        df_filtered["geo"],
        df_filtered["mio_eur"],
        color=config.TEAL_PALETTE["teal_3"],
    )

    plt.xlabel("Disability benefit expenditure (millions of euros)")
    plt.title(
        "Social Protection Expenditure on Disability Benefits by Country (2023)\n(Total scheme, all benefit types, millions of euros)"
    )
    plt.tight_layout()
