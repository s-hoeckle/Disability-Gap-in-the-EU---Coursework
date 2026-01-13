#colour palette for this project:
#teal sequence light to dark
#b5d1ae teal 1
#80ae9a teal 2
#568b87 teal 3
#326b77 teal 4
#1b485e teal 5
#122740 teal 6

import pandas as pd

# Pandas display options
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

# -------------------------------------------------------------------
# Load datasets
# -------------------------------------------------------------------
gbv_datasets = {
    "any": pd.read_csv("estat_gbv_any_lim.tsv", sep="\t"),
    "dv": pd.read_csv("estat_gbv_dv_lim.tsv", sep="\t"),
    "ipv": pd.read_csv("estat_gbv_ipv_lim.tsv", sep="\t"),
    "npv": pd.read_csv("estat_gbv_npv_lim.tsv", sep="\t"),
}

edat_datasets = {
    "edu": pd.read_csv("estat_edat_lfs_9920.tsv", sep="\t"),
}

# -------------------------------------------------------------------
# Common processing function
# -------------------------------------------------------------------
def process_gbv(df):
    # Split the combined column into separate columns
    df[['freq', 'lev_limit', 'unit', 'geo']] = (
        df['freq,lev_limit,unit,geo\\TIME_PERIOD']
        .str.split(',', expand=True)
    )

    # Rename the value column (year)
    df = df.rename(columns={'2021 ': 'disability_rate'})

    # Keep only relevant columns
    df = df[['geo', 'lev_limit', 'disability_rate']]

    df['disability_rate'] = df['disability_rate'].astype(str).str.extract(r'(\d+\.?\d*)')[0]

    # Convert disability_rate to numeric
    df['disability_rate'] = pd.to_numeric(df['disability_rate'], errors='coerce')

    return df

# -------------------------------------------------------------------
# Apply processing to all gbv_datasets
# -------------------------------------------------------------------
gbv_datasets = {name: process_gbv(df) for name, df in gbv_datasets.items()}

# Optional: unpack back into individual variables
any = gbv_datasets["any"]
dv = gbv_datasets["dv"]
ipv = gbv_datasets["ipv"]
npv = gbv_datasets["npv"]

# -------------------------------------------------------------------
# Describe gbv_datasets
# -------------------------------------------------------------------
for name, df in gbv_datasets.items():
    print(f"\n{name.upper()} DATASET DESCRIPTION")
    print(df.describe())

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load dataset
df = pd.read_csv("estat_gbv_any_lim.tsv", sep="\t")

# Split combined column
df[['freq', 'lev_limit', 'unit', 'geo']] = (
    df['freq,lev_limit,unit,geo\\TIME_PERIOD']
    .str.split(',', expand=True)
)

# Rename and convert value column
df = df.rename(columns={'2021 ': 'disability_rate'})
df['disability_rate'] = df['disability_rate'].astype(str).str.extract(r'(\d+\.?\d*)')[0]
df['disability_rate'] = pd.to_numeric(df['disability_rate'], errors='coerce')

# Keep only severity categories (exclude TOTAL and EU average)
severity_levels = ['SOME', 'SM_SEV', 'SEV','NONE']
df = df[
    (df['lev_limit'].isin(severity_levels)) &
    (df['geo'] != 'EU_V')
]

# Pivot data so each severity level becomes a column
df_pivot = df.pivot(index='geo', columns='lev_limit', values='disability_rate')

# Sort countries by no disability value for readability
df_pivot = df_pivot.sort_values('NONE')

# Plot settings
group_spacing = 1.3
y = np.arange(len(df_pivot)) * group_spacing
bar_height = 0.25

plt.figure(figsize=(12, 10))


colors = {
    'NONE': '#122740',  # teal 6
    'SOME':   '#326b77',  # teal 4
    'SM_SEV': '#568b87',  # teal 3
    'SEV':    '#b5d1ae'   # teal 1
}




plt.barh(y - 2*bar_height, df_pivot['NONE'],
         height=bar_height, label='No limitation in activity',
         color=colors['NONE'])

plt.barh(y - bar_height, df_pivot['SOME'],
         height=bar_height, label='Some limitation in activity',
         color=colors['SOME'])

plt.barh(y, df_pivot['SM_SEV'],
         height=bar_height, label='Some or severe limitation in activity',
         color=colors['SM_SEV'])

plt.barh(y + bar_height, df_pivot['SEV'],
         height=bar_height, label='Severe limitation in activity',
         color=colors['SEV'])



plt.yticks(y, df_pivot.index)
plt.xlabel("Reported violence (%)")
plt.ylabel("Country")
plt.title("Women who have experiences violence by any partner by level of disability (2021)")
plt.legend()
plt.tight_layout()
plt.show()
