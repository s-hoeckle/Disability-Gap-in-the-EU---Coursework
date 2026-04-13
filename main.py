import matplotlib.pyplot as plt
import config
import data_loader
import graph_violence_disability_levels
import graph_violence_gap
import graph_edu_gap_uni
import graph_edu_gap_primary
import graph_correlation_uni
import graph_correlation_broad
import graph_correlation_primary
import graph_poverty_disability_gap
import graph_holiday_disability_gap

if __name__ == "__main__":
    print("--- Starting Analysis ---")

    print(f"Loading GBV data from {config.FILES['gbv_any']}...")
    gbv_df = data_loader.process_gbv_data(config.FILES["gbv_any"])

    print(f"Loading Education data from {config.FILES['education']}...")
    edu_df = data_loader.process_education_data(config.FILES["education"])

    print(f"Loading Health data from {config.FILES['health']}...")
    health_df = data_loader.process_health_data(config.FILES["health"])

    print("Generating Graph 1: Violence by Severity Level...")
    graph_violence_disability_levels.plot(gbv_df)

    print("Generating Graph 2: Violence Risk Gap...")
    graph_violence_gap.plot(gbv_df)

    print("Generating Graph 3: Education Gap...")
    graph_edu_gap_uni.plot(edu_df)

    print("Generating Graph 4: Correlation Analysis for University level...")
    graph_correlation_uni.plot(gbv_df, edu_df)

    print("Generating Graph 5: Primary Education Gap...")
    graph_edu_gap_primary.plot(edu_df)

    print("Generating Graph 6: Broad Education Gap Correlation Analysis...")
    graph_correlation_broad.plot(gbv_df, edu_df)

    print("Generating Graph 7: Primary Education Gap Correlation Analysis...")
    graph_correlation_primary.plot(gbv_df, edu_df)

    print("Generating Graph 8: Poverty/Social Exclusion Disability Gap...")
    graph_poverty_disability_gap.plot(health_df)

    print(f"Loading Holiday data from {config.FILES['holiday']}...")
    holiday_df = data_loader.process_holiday_data(config.FILES["holiday"])

    print("Generating Graph 9: Holiday Affordability Disability Gap...")
    graph_holiday_disability_gap.plot(holiday_df)

    plt.show()

    print("--- Analysis Complete ---")
