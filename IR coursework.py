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
    df = df.rename(columns={'2021 ': 'abuse_rate_%'})

    # Keep only relevant columns
    df = df[['geo', 'lev_limit', 'abuse_rate_%']]

    df['abuse_rate_%'] = df['abuse_rate_%'].astype(str).str.extract(r'(\d+\.?\d*)')[0]

    # Convert abuse_rate_% to numeric
    df['abuse_rate_%'] = pd.to_numeric(df['abuse_rate_%'], errors='coerce')

    return df

# -------------------------------------------------------------------
# Apply processing to all gbv_datasets
# -------------------------------------------------------------------
gbv_datasets = {name: process_gbv(df) for name, df in gbv_datasets.items()}

gbv_any = gbv_datasets["any"]
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
df = df.rename(columns={'2021 ': 'abuse_rate_%'})
df['abuse_rate_%'] = df['abuse_rate_%'].astype(str).str.extract(r'(\d+\.?\d*)')[0]
df['abuse_rate_%'] = pd.to_numeric(df['abuse_rate_%'], errors='coerce')

# Keep only severity categories (exclude TOTAL and EU average)
severity_levels = ['TOTAL','SOME', 'SEV', 'SM_SEV','NONE']
df = df[
    (df['lev_limit'].isin(severity_levels)) &
    (df['geo'] != 'EU_V')
]



# Pivot data so each severity level becomes a column
df_pivot = df.pivot(index='geo', columns='lev_limit', values='abuse_rate_%')

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
    'SEV':    '#b5d1ae'   # teal 1
}



# 1. NONE 
plt.barh(y - bar_height, df_pivot['NONE'],
         height=bar_height, label='No limitation in activity',
         color=colors['NONE'])

# 2. SOME 
plt.barh(y, df_pivot['SOME'],
         height=bar_height, label='Some limitation in activity',
         color=colors['SOME'])

# 3. SEV 
plt.barh(y + bar_height, df_pivot['SEV'],
         height=bar_height, label='Severe limitation in activity',
         color=colors['SEV'])


plt.yticks(y, df_pivot.index)
plt.xlabel("Reported violence (%)")
plt.ylabel("Country")
plt.title("Women who have experienced violence by any partner by level of disability (2021)")
plt.legend()
plt.tight_layout()
plt.show()

#-------------------------------------------------------------------------
# calculate abuse gap between victims with disability and those without 
#-------------------------------------------------------------------------

# columns 'NONE' and 'SM_SEV'
df_pivot['diff_gap'] = df_pivot['SM_SEV'] - df_pivot['NONE']
df_pivot = df_pivot.sort_values('diff_gap', ascending=True)

# Plot settings
y = np.arange(len(df_pivot))
bar_height = 0.35  

plt.figure(figsize=(12, 10))

# Plot 'NONE' (Baseline)
plt.barh(y - bar_height/2, df_pivot['NONE'],
         height=bar_height, label='No limitation (NONE)',
         color='#b5d1ae') # Teal 1 

# Plot 'SM_SEV' (Comparison)
plt.barh(y + bar_height/2, df_pivot['SM_SEV'],
         height=bar_height, label='Some or severe limitation (SM_SEV)',
         color='#326b77') # Teal 4 

# Add the difference value as text next to the bars
for i, (idx, row) in enumerate(df_pivot.iterrows()):
    gap = row['diff_gap']
    # Place text at the end of the SM_SEV bar
    plt.text(row['SM_SEV'] + 1, i + bar_height/2, 
             f"+{gap:.1f} pp", 
             va='center', fontsize=9, color='#326b77')

plt.yticks(y, df_pivot.index)
plt.xlabel("Reported violence (%)")
plt.title("Disability Risk Gap: Difference in violence reported by women\nwith 'Some or Severe' limitations vs 'No' limitations")
plt.legend()
plt.tight_layout()
plt.show()
#------------------------------------------------------------------------------------
#claculate university education gap between disabled and able bodied people in the eu countries
#-------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------
# NEW SECTION: University Education Gap (15-74) - Disabled vs Able-bodied
# ------------------------------------------------------------------------------------

# Configuration for Education Data
EDU_FILE = "estat_edat_lfs_9920.tsv"
AGE_TARGET = 'Y15-74'       # Target Age (Will fallback to Y15-64 if missing)
EDU_LEVEL = 'ED5-8'         # Tertiary Education (University degrees)
DISABILITY_CODE = 'SM_SEV'      # "Limited" = Aggregate of Some + Severe
ABLE_CODE = 'NONE'          # No limitation

def analyze_education_gap(filepath):
    # 1. Robust Load (Handles variable column counts)
    df = pd.read_csv(filepath, sep="\t")
    
    # Split the first column (the composite key)
    split_df = df.iloc[:, 0].str.split(',', expand=True)
    
    # Auto-detect column names
    col_map = {}
    for col in split_df.columns:
        # Sample the column to guess its content
        val_sample = split_df[col].dropna().unique().astype(str)
        
        # Check based on content patterns
        # Using .str.contains().any() is safe even if you have a variable named 'any'
        if pd.Series(val_sample).str.contains('Y15').any():
            col_map[col] = 'age'
        elif pd.Series(val_sample).str.contains('ED5|ED3').any():
            col_map[col] = 'isced11'
        elif pd.Series(val_sample).str.contains('SM_SEV|NONE').any():
            col_map[col] = 'disability_status'
        elif pd.Series(val_sample).isin(['T', 'M', 'F']).any():
            col_map[col] = 'sex'
            
    split_df = split_df.rename(columns=col_map)
    
    # Assume last split column is Geo if not found
    if 'geo' not in split_df.columns:
        split_df = split_df.rename(columns={split_df.columns[-1]: 'geo'})
    
    # Combine with the value column (last column of original file)
    df_clean = pd.concat([split_df, df.iloc[:, -1]], axis=1)
    df_clean.columns = list(split_df.columns) + ['value']
    
    # Clean numeric values
    df_clean['value'] = df_clean['value'].astype(str).str.extract(r'(\d+\.?\d*)')[0]
    df_clean['value'] = pd.to_numeric(df_clean['value'], errors='coerce')
    
    return df_clean

# Load Data
df_edu = analyze_education_gap(EDU_FILE)

# Check if Age Y15-74 exists, otherwise fallback to Y15-64
available_ages = df_edu['age'].unique()
current_age_filter = AGE_TARGET
if AGE_TARGET not in available_ages:
    print(f"Note: {AGE_TARGET} not found in data. Switching to 'Y15-64'.")
    current_age_filter = 'Y15-64'

# 2. Filter Data
df_edu_filtered = df_edu[
    (df_edu['age'] == current_age_filter) &
    (df_edu['isced11'] == EDU_LEVEL) &
    (df_edu['sex'] == 'T') &            # Total (Men + Women)
    (df_edu['geo'].str.len() == 2) &    # Countries only
    (df_edu['disability_status'].isin([ABLE_CODE, DISABILITY_CODE]))
].copy()

# 3. Pivot and Calculate Gap
df_edu_pivot = df_edu_filtered.pivot(index='geo', columns='disability_status', values='value')

# Calculate Gap: (Able Bodied % - Disabled %)
# Positive Gap = Able-bodied people are more likely to have a degree
df_edu_pivot['edu_gap'] = df_edu_pivot[ABLE_CODE] - df_edu_pivot[DISABILITY_CODE]

# Sort by gap size
df_edu_pivot = df_edu_pivot.sort_values('edu_gap', ascending=True).dropna(subset=['edu_gap'])

# 4. Plotting
plt.figure(figsize=(12, 10))
y = np.arange(len(df_edu_pivot))
bar_height = 0.35

# Plot
#plt.barh(y, df_edu_pivot['edu_gap'], height=bar_height, color='#326b77') # Teal 4

# Plot 'NONE' (Baseline)
plt.barh(y - bar_height/2, df_edu_pivot['NONE'],
         height=bar_height, label='No limitation (NONE)',
         color='#b5d1ae') # Teal 1 (Light)

# Plot 'SM_SEV' (Comparison)
plt.barh(y + bar_height/2, df_edu_pivot['SM_SEV'],
         height=bar_height, label='Some or severe limitation (SM_SEV)',
         color='#326b77') # Teal 4 (Darker)


# Add labels
for i, gap in enumerate(df_edu_pivot['edu_gap']):
    plt.text(gap + 0.5, i, f"+{gap:.1f} pp", va='center', fontsize=9, color='#122740')

plt.yticks(y, df_edu_pivot.index)
plt.xlabel("Percentage Point Gap (Able-bodied Rate - Disabled Rate)")
plt.title(f"University Education Gap (Age {current_age_filter})\nExcess rate of degrees held by able-bodied vs. disabled people")

# Styling
plt.grid(axis='x', linestyle='--', alpha=0.5)
plt.gca().spines['top'].set_visible(False)
plt.gca().spines['right'].set_visible(False)
plt.gca().spines['left'].set_visible(False)
plt.legend()
plt.tight_layout()
plt.show()
