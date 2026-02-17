import polars as pl
import matplotlib.pyplot as plt
import seaborn as sns


lazy_df = pl.scan_csv("../data/micro_events.csv")

# 1. Filter for Blood Cultures
blood_culture_lazy = lazy_df.filter(
    pl.col("spec_type_desc").str.contains("(?i)blood")
)

# 2. Count occurrences for each Organism/Antibiotic pair
# This helps identify if a test was actually performed
heatmap_data = (
    blood_culture_lazy
    .select(["org_name", "ab_name"])
    .filter(pl.col("org_name").is_not_null() & pl.col("ab_name").is_not_null())
    .group_by(["org_name", "ab_name"])
    .len()  # Count how many tests exist for this pair
    .collect()
)

# 3. Pivot the data to create a matrix
# Antibiotics as rows, Organisms as columns
pivot_df = (
    heatmap_data
    .pivot(on="org_name", index="ab_name", values="len")
    .to_pandas()
    .set_index("ab_name")
)

# 4. Optional: Filter for the most frequent data to keep the plot readable
# We'll take the top 40 organisms and top 50 antibiotics
top_orgs = pivot_df.sum(axis=0).sort_values(ascending=False).head(40).index
top_abs = pivot_df.sum(axis=1).sort_values(ascending=False).head(50).index
subset_df = pivot_df.loc[top_abs, top_orgs]

# 5. Plotting the Heatmap
plt.figure(figsize=(20, 12))

# We use a boolean check (subset_df > 0) to show Presence vs Absence
# Or you can plot subset_df directly with a log scale to see frequency
sns.heatmap(
    subset_df.notnull(), 
    cmap="YlGnBu", 
    cbar=False, 
    linewidths=.1,
    linecolor='gray'
)

plt.title("Antibiogram Data Presence (Blood Cultures)\nColored = Test Performed | White = Null (Missing Data)", fontsize=16)
plt.xlabel("Organism Name", fontsize=12)
plt.ylabel("Antibiotic Name", fontsize=12)
plt.xticks(rotation=45, ha='right')
plt.tight_layout()

plt.savefig("../Figures/sensitivity_heatmap.png")
plt.show()