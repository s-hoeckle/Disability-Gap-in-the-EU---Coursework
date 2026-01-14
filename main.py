# main.py
import config
import data_loader
import graph_violence_disability_levels
import graph_violence_gap
import graph_edu_gap
import graph_correlation
import graph_correlation_broad
import graph_correlation_primary

def main():
    print("--- Starting Analysis ---")

    # 1. Load Data
    print(f"Loading GBV data from {config.FILES['gbv_any']}...")
    gbv_df = data_loader.process_gbv_data(config.FILES['gbv_any'])

    print(f"Loading Education data from {config.FILES['education']}...")
    edu_df = data_loader.process_education_data(config.FILES['education'])

    # 2. Generate Plots
    print("Generating Graph 1: Violence by Severity Level...")
    graph_violence_disability_levels.plot(gbv_df)

    print("Generating Graph 2: Violence Risk Gap...")
    graph_violence_gap.plot(gbv_df)

    print("Generating Graph 3: Education Gap...")
    graph_edu_gap.plot(edu_df)

    print("Generating Graph 4: Correlation Analysis for University level...") 
    graph_correlation.plot(gbv_df, edu_df)

    print("Generating Graph 5: Broad Education Gap Correlation Analysis...")
    graph_correlation_broad.plot(gbv_df, edu_df)

    print("Generating Graph 6: Primary Education Gap Correlation Analysis...")
    graph_correlation_primary.plot(gbv_df, edu_df)

    
if __name__ == "__main__":
    main()

    print("--- Analysis Complete ---")

