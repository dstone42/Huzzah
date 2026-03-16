import polars as pl
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# 1. Load and process data
lazy_df = pl.scan_csv("../data/micro_events.csv")

# Filter for blood cultures and calculate percentages
antibiogram_df = (
    lazy_df
    .filter(pl.col("spec_type_desc").str.contains("(?i)blood"))
    .filter(pl.col("org_name").is_not_null() & pl.col("ab_name").is_not_null())
    .group_by(["ab_name", "org_name"])
    .agg(
        ((pl.col("interpretation").str.to_uppercase() == "S").mean() * 100).alias("pct_sensitive")
    )
    .collect()
    .pivot(on="org_name", index="ab_name", values="pct_sensitive")
    .sort("ab_name")
)

# Convert to pandas for plotting
# We fill NaNs with a specific value if we want a custom color, 
# but setting the axis facecolor to black is cleaner for "missing" data.
plot_df = antibiogram_df.to_pandas().set_index("ab_name")

# 2. Setup the Plot
# Calculate dynamic size: roughly 0.5 inches per column/row to keep it readable
width = max(15, len(plot_df.columns) * 0.4)
height = max(10, len(plot_df.index) * 0.4)

plt.figure(figsize=(width, height))

# Set the background (the "under" color) to black
sns.set_theme(rc={'axes.facecolor': 'black'})

# 3. Create Heatmap
# cmap="RdYlGn" is Red-Yellow-Green (0=Red, 100=Green)
ax = sns.heatmap(
    plot_df, 
    cmap="RdYlGn", 
    annot=True,          # Show the actual percentages in the cells
    fmt=".0f",           # No decimals for clarity
    linewidths=.5, 
    linecolor="#333333", # Dark grey lines between cells
    cbar_kws={'label': '% Sensitive'},
    vmin=0,              # Ensure 0 is the floor for Red
    vmax=100             # Ensure 100 is the ceiling for Green
)

# 4. Formatting
plt.title("Comprehensive Blood Culture Antibiogram (% Sensitive)", fontsize=20, pad=20)
plt.xlabel("Organism Name", fontsize=14)
plt.ylabel("Antibiotic Name", fontsize=14)

# Move X-axis labels to the top for easier reading if the list is long
ax.xaxis.tick_top()
ax.xaxis.set_label_position('top') 
plt.xticks(rotation=45, ha='left')

plt.tight_layout()
plt.savefig("full_antibiogram_heatmap.png", dpi=300)
plt.show()