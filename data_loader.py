import pandas as pd
import config


def process_gbv_data(filepath):
    df = pd.read_csv(filepath, sep="\t")

    split_cols = df.iloc[:, 0].str.split(",", expand=True)

    split_cols.columns = ["freq", "lev_limit", "unit", "geo"]

    df = pd.concat([split_cols, df.iloc[:, 1:]], axis=1)

    val_col = [c for c in df.columns if "2021" in c][0]
    df = df.rename(columns={val_col: "abuse_rate_%"})

    df["abuse_rate_%"] = df["abuse_rate_%"].astype(str).str.extract(r"(\d+\.?\d*)")[0]
    df["abuse_rate_%"] = pd.to_numeric(df["abuse_rate_%"], errors="coerce")

    df = df[
        (df["lev_limit"].isin(config.SEVERITY_LEVELS))
        & (~df["geo"].isin(config.EXCLUDED_GEO))
    ]

    return df


def process_health_data(filepath):
    df = pd.read_csv(filepath, sep="\t")

    split_cols = df.iloc[:, 0].str.split(",", expand=True)
    split_cols.columns = ["freq", "unit", "lev_limit", "age", "sex", "geo"]

    df = pd.concat([split_cols, df.iloc[:, 1:]], axis=1)

    val_col = [c for c in df.columns if "2021" in c][0]
    df = df.rename(columns={val_col: "health_rate_%"})

    df["health_rate_%"] = df["health_rate_%"].astype(str).str.extract(r"(\d+\.?\d*)")[0]
    df["health_rate_%"] = pd.to_numeric(df["health_rate_%"], errors="coerce")

    df = df[~df["geo"].isin(config.EXCLUDED_GEO)]

    return df


def process_holiday_data(filepath):
    df = pd.read_csv(filepath)

    df = df.rename(columns={
        "disability_level": "lev_limit",
        "age_group": "age",
        "country": "geo",
        "2021": "holiday_rate_%",
    })

    df["holiday_rate_%"] = pd.to_numeric(df["holiday_rate_%"], errors="coerce")

    df = df[~df["geo"].isin(config.EXCLUDED_GEO)]

    return df


def process_education_data(filepath):
    df = pd.read_csv(filepath, sep="\t")

    split_df = df.iloc[:, 0].str.split(",", expand=True)

    col_map = {}
    for col in split_df.columns:
        val_sample = split_df[col].dropna().unique().astype(str)
        if pd.Series(val_sample).str.contains("Y15").any():
            col_map[col] = "age"
        elif pd.Series(val_sample).str.contains("ED5|ED3").any():
            col_map[col] = "isced11"
        elif pd.Series(val_sample).str.contains("SM_SEV|NONE").any():
            col_map[col] = "disability_status"
        elif pd.Series(val_sample).isin(["T", "M", "F"]).any():
            col_map[col] = "sex"

    split_df = split_df.rename(columns=col_map)

    if "geo" not in split_df.columns:
        split_df = split_df.rename(columns={split_df.columns[-1]: "geo"})

    df_clean = pd.concat([split_df, df.iloc[:, -1]], axis=1)
    df_clean.columns = list(split_df.columns) + ["value"]

    df_clean["value"] = df_clean["value"].astype(str).str.extract(r"(\d+\.?\d*)")[0]
    df_clean["value"] = pd.to_numeric(df_clean["value"], errors="coerce")

    return df_clean
