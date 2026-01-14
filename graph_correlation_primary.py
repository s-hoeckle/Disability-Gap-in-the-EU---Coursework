import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import config
from scipy import stats

def get_violence_gap(df):
    """Helper to calculate violence gap per country"""
    pivot = df.pivot(index='geo', columns='lev_limit', values='abuse_rate_%')
    gap_series = pivot['SM_SEV'] - pivot['NONE']
    return gap_series.rename("violence_gap")

def get_broad_education_gap(df):
    """
    Calculates the gap for 'Below Upper Secondary' (ISCED 0-2).
    'ED 0-2' for Women ('F').
    """
    conf = config.EDU_CONFIG
    
   
    available_ages = df['age'].unique()
    age_filter = conf['target_age'] if conf['target_age'] in available_ages else conf['fallback_age']
    
    # 2. Define Broad Levels (Upper Secondary + Tertiary)
    broad_levels = ['ED0-2',] 

    # 3. Filter Data
    # Note: We switch sex to 'F' to specifically look at women's education gap 
    # to match the women-only violence data.
    mask = (
        (df['age'] == age_filter) &
        (df['isced11'].isin(broad_levels)) & 
        (df['sex'] == 'F') &                 
        (df['geo'].str.len() == 2) &
        (df['disability_status'].isin([conf['able_code'], conf['disability_code']]))
    )
    df_filtered = df[mask].copy()
    
    # 4. Aggregation
    # Since we have two education rows per country (ED3_4 and ED5-8), 
    # we group by country and disability status and SUM the percentages.
    df_aggr = df_filtered.groupby(['geo', 'disability_status'])['value'].sum().reset_index()

    # 5. Pivot
    pivot = df_aggr.pivot(index='geo', columns='disability_status', values='value')
    
    # Gap = Able Rate - Disabled Rate
    gap_series = pivot[conf['able_code']] - pivot[conf['disability_code']]
    return gap_series.rename("broad_edu_gap")

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
    Plots correlation: Broad Education Gap (Women) vs Violence Risk Gap.
    """
    # 1. Prepare Data
    v_gap = get_violence_gap(gbv_df)
    e_gap = get_broad_education_gap(edu_df)

    # 2. Merge & Clean
    df = pd.concat([v_gap, e_gap], axis=1, join='inner').dropna()
    df = remove_outliers(df, columns=['violence_gap', 'broad_edu_gap'], threshold=3.0)

    # 3. Setup Plot
    plt.figure(figsize=(10, 8))
    
    plt.scatter(df['broad_edu_gap'], df['violence_gap'], 
                color=config.TEAL_PALETTE['teal_4'], 
                s=100, alpha=0.8, edgecolors='white', zorder=2)

    # Labels
    for country, row in df.iterrows():
        plt.text(row['broad_edu_gap'] + 0.2, row['violence_gap'] + 0.2, 
                 country, fontsize=9, color=config.TEAL_PALETTE['teal_6'])

    # Trend Line
    if len(df) > 1:
        z = np.polyfit(df['broad_edu_gap'], df['violence_gap'], 1)
        p = np.poly1d(z)
        
        x_range = np.linspace(df['broad_edu_gap'].min(), df['broad_edu_gap'].max(), 100)
        plt.plot(x_range, p(x_range), 
                 color=config.TEAL_PALETTE['teal_2'], 
                 linestyle='--', linewidth=2, label='Trend Line', zorder=1)

        corr = df['broad_edu_gap'].corr(df['violence_gap'])
        plt.legend([f"Trend (r = {corr:.2f})"])

    # 4. Styling
    plt.title("Correlation: Education Inequality (Upper Secondary -) vs. Violence Risk Gap\n(Subset: Women Only)")
    plt.xlabel("Education Gap (pp)\n(Inequality in attaining Primary or lower secondary education)")
    plt.ylabel("Violence Risk Gap (pp)\n(Excess reports of violence by disabled women)")
    
    plt.grid(True, linestyle='--', alpha=0.3, color='gray')
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)

    plt.tight_layout()
    plt.show()
