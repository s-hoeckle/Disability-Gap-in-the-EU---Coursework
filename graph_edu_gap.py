# plot_education_gap.py
import matplotlib.pyplot as plt
import numpy as np
import config

def plot(df):
    """
    Plots the university education gap between able-bodied 
    and disabled people.
    """
    conf = config.EDU_CONFIG
    
    # Determine available age range
    available_ages = df['age'].unique()
    age_filter = conf['target_age'] if conf['target_age'] in available_ages else conf['fallback_age']
    
    if age_filter != conf['target_age']:
        print(f"Notice: {conf['target_age']} not found. Using {age_filter}")

    # Filter
    mask = (
        (df['age'] == age_filter) &
        (df['isced11'] == conf['level']) &
        (df['sex'] == 'T') &
        (df['geo'].str.len() == 2) & # Countries only (2 chars)
        (df['disability_status'].isin([conf['able_code'], conf['disability_code']]))
    )
    df_filtered = df[mask].copy()

    # Pivot
    df_pivot = df_filtered.pivot(index='geo', columns='disability_status', values='value')
    
    # Calc Gap
    df_pivot['edu_gap'] = df_pivot[conf['able_code']] - df_pivot[conf['disability_code']]
    df_pivot = df_pivot.sort_values('edu_gap', ascending=True).dropna(subset=['edu_gap'])

    y = np.arange(len(df_pivot))
    h = config.PLOT_SETTINGS['bar_height_gap']

    plt.figure(figsize=config.PLOT_SETTINGS['figsize'])

    # Plot 'NONE' (Baseline) - Light
    plt.barh(y - h/2, df_pivot[conf['able_code']], height=h, 
             label='No limitation (NONE)', color=config.TEAL_PALETTE['teal_1'])

    # Plot 'SM_SEV' (Comparison) - Dark
    plt.barh(y + h/2, df_pivot[conf['disability_code']], height=h, 
             label='Some or severe limitation (SM_SEV)', color=config.TEAL_PALETTE['teal_4'])

    # Annotations
    for i, gap in enumerate(df_pivot['edu_gap']):
        plt.text(gap + 0.5, i, f"+{gap:.1f} pp", va='center', fontsize=9, color=config.TEAL_PALETTE['teal_6'])

    plt.yticks(y, df_pivot.index)
    plt.xlabel("Percentage Point Gap")
    plt.title(f"University Education Gap ({age_filter})\nExcess rate of degrees held by able-bodied vs. disabled people")
    
    # Styling
    plt.grid(axis='x', linestyle='--', alpha=0.5)
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['left'].set_visible(False)
    plt.legend()
    plt.tight_layout()
    plt.show()