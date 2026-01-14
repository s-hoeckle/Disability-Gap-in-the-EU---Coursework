# graph_correlation.py
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import config
from scipy import stats

def get_violence_gap(df):
    """Helper to calculate violence gap per country"""
    pivot = df.pivot(index='geo', columns='lev_limit', values='abuse_rate_%')
    # Gap = Disabled Rate - Able-bodied Rate (Positive = Higher risk for disabled)
    gap_series = pivot['SM_SEV'] - pivot['NONE']
    return gap_series.rename("violence_gap")

def get_education_gap(df):
    """Helper to calculate education gap per country"""
    conf = config.EDU_CONFIG
    
    # 1. Filter for correct age/level
    available_ages = df['age'].unique()
    age_filter = conf['target_age'] if conf['target_age'] in available_ages else conf['fallback_age']
    
    mask = (
        (df['age'] == age_filter) &
        (df['isced11'] == conf['tet_level']) &
        (df['sex'] == 'T') &
        (df['geo'].str.len() == 2) &
        (df['disability_status'].isin([conf['able_code'], conf['disability_code']]))
    )
    df_filtered = df[mask].copy()
    
    # 2. Pivot
    pivot = df_filtered.pivot(index='geo', columns='disability_status', values='value')
    
    # Gap = Able Rate - Disabled Rate (Positive = Higher inequality)
    gap_series = pivot[conf['able_code']] - pivot[conf['disability_code']]
    return gap_series.rename("edu_gap")

def remove_outliers(df, columns, threshold=3.0):
    z_scores = np.abs(stats.zscore(df[columns]))
    

    df_clean = df[(z_scores < threshold).all(axis=1)]
    
    removed = df.index.difference(df_clean.index).tolist()
    if removed:
        print(f"--- Outliers Removed (Threshold {threshold}) ---")
        print(f"Countries: {', '.join(removed)}")
        
    return df_clean

def plot(gbv_df, edu_df):
    """
    Plots a scatter graph correlating Education Gap vs Violence Gap.
    """
    # 1. Prepare Data
    v_gap = get_violence_gap(gbv_df)
    e_gap = get_education_gap(edu_df)

    # 2. Merge on Country Code (geo)
    # Inner join keeps only countries present in BOTH datasets
    df = pd.concat([v_gap, e_gap], axis=1, join='inner').dropna()
    df = remove_outliers(df, columns=['violence_gap', 'edu_gap'], threshold=3.0)

    # 3. Setup Plot
    plt.figure(figsize=(10, 8))
    
    # Scatter Points
    plt.scatter(df['edu_gap'], df['violence_gap'], 
                color=config.TEAL_PALETTE['teal_4'], 
                s=100, alpha=0.8, edgecolors='white', zorder=2)

    # 4. Add Country Labels
    # We create a slight offset so text doesn't overlap the dot
    for country, row in df.iterrows():
        plt.text(row['edu_gap'] + 0.2, row['violence_gap'] + 0.2, 
                 country, fontsize=9, color=config.TEAL_PALETTE['teal_6'])

    # 5. Add Trend Line (Linear Regression)
    if len(df) > 1:
        z = np.polyfit(df['edu_gap'], df['violence_gap'], 1)
        p = np.poly1d(z)
        
        # Plot line across the full range of x
        x_range = np.linspace(df['edu_gap'].min(), df['edu_gap'].max(), 100)
        plt.plot(x_range, p(x_range), 
                 color=config.TEAL_PALETTE['teal_2'], 
                 linestyle='--', linewidth=2, label='Trend Line', zorder=1)

        # Calculate Correlation Coefficient (r)
        corr = df['edu_gap'].corr(df['violence_gap'])
        plt.legend([f"Trend (r = {corr:.2f})"])

    # 6. Styling
    plt.title("Correlation: Education Inequality (University level) vs. Violence Risk Gap")
    plt.xlabel("Education Gap (pp)\n(Higher = More inequality in degrees)")
    plt.ylabel("Violence Risk Gap (pp)\n(Higher = Greater excess reports of violence by disabled women)")
    
    # Add grid for readability in scatter plots
    plt.grid(True, linestyle='--', alpha=0.3, color='gray')
    
    # Remove top/right spines
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)

    plt.tight_layout()
    plt.show()

    #graph 2 - correlation in women with upper secondary education

