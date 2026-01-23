import config
import numpy as np
from scipy import stats


def get_violence_gap(df):
    pivot = df.pivot(index="geo", columns="lev_limit", values="abuse_rate_%")
    gap_series = pivot["SM_SEV"] - pivot["NONE"]
    return gap_series.rename("violence_gap")


def get_education_gap(df):
    conf = config.EDU_CONFIG

    available_ages = df["age"].unique()
    age_filter = (
        conf["target_age"]
        if conf["target_age"] in available_ages
        else conf["fallback_age"]
    )

    mask = (
        (df["age"] == age_filter)
        & (df["isced11"] == conf["tet_level"])
        & (df["sex"] == "T")
        & (df["geo"].str.len() == 2)
        & (df["disability_status"].isin([conf["able_code"], conf["disability_code"]]))
    )
    df_filtered = df[mask].copy()

    pivot = df_filtered.pivot(index="geo", columns="disability_status", values="value")

    gap_series = pivot[conf["able_code"]] - pivot[conf["disability_code"]]
    return gap_series.rename("edu_gap")


def get_broad_education_gap(df):
    conf = config.EDU_CONFIG

    available_ages = df["age"].unique()
    age_filter = (
        conf["target_age"]
        if conf["target_age"] in available_ages
        else conf["fallback_age"]
    )

    broad_levels = ["ED3_4", "ED5-8"]

    mask = (
        (df["age"] == age_filter)
        & (df["isced11"].isin(broad_levels))
        & (df["sex"] == "F")
        & (df["geo"].str.len() == 2)
        & (df["disability_status"].isin([conf["able_code"], conf["disability_code"]]))
    )
    df_filtered = df[mask].copy()

    df_aggr = (
        df_filtered.groupby(["geo", "disability_status"])["value"].sum().reset_index()
    )

    pivot = df_aggr.pivot(index="geo", columns="disability_status", values="value")

    gap_series = pivot[conf["able_code"]] - pivot[conf["disability_code"]]
    return gap_series.rename("broad_edu_gap")


def remove_outliers(df, columns, threshold=3.0):
    z_scores = np.abs(stats.zscore(df[columns]))
    df_clean = df[(z_scores < threshold).all(axis=1)]

    removed = df.index.difference(df_clean.index).tolist()
    if removed:
        print(f"--- Outliers Removed (Threshold {threshold}) ---")
        print(f"Countries: {', '.join(removed)}")

    return df_clean