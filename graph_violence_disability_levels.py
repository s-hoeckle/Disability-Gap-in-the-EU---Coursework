# graph_violence_levels.py
import matplotlib.pyplot as plt
import numpy as np
import config

def plot(df):
    severity_levels = ['TOTAL','SOME', 'SEV', 'SM_SEV','NONE']
    df_filtered = df[
        (df['lev_limit'].isin(severity_levels)) & (df['geo'] != 'EU_V')
    ].copy()

    # Safety: handle duplicates before pivot
    df_filtered = df_filtered.groupby(['geo', 'lev_limit'], as_index=False)['abuse_rate_%'].mean()
    df_pivot = df_filtered.pivot(index='geo', columns='lev_limit', values='abuse_rate_%')
    df_pivot = df_pivot.sort_values('NONE')

    group_spacing = 1.3
    y = np.arange(len(df_pivot)) * group_spacing
    bar_height = 0.25

    plt.figure(figsize=(12, 10))
    plt.barh(y - bar_height, df_pivot['NONE'], height=bar_height, 
             label='No limitation in activity', color=config.COLORS['NONE'])
    plt.barh(y, df_pivot['SOME'], height=bar_height, 
             label='Some limitation in activity', color=config.COLORS['SOME'])
    plt.barh(y + bar_height, df_pivot['SEV'], height=bar_height, 
             label='Severe limitation in activity', color=config.COLORS['SEV'])

    plt.yticks(y, df_pivot.index)
    plt.xlabel("Reported violence (%)")
    plt.ylabel("Country")
    plt.title("Women who have experienced violence by any partner by level of disability (2021)")
    plt.legend()
    plt.tight_layout()
    plt.show()
    return df_pivot # Returning pivot for the gap calculation