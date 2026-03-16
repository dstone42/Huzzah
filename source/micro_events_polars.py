import polars as pl
import matplotlib.pyplot as plt
import seaborn as sns

# load the data from data/micro_events.csv
lazy_df = pl.scan_csv("../data/micro_events.csv")

print(lazy_df.collect_schema())


## get all the blood cultures
# blood_cultures = (
#     lazy_df
#     .with_columns(
#         pl.col("spec_type_desc").str.strip_chars().str.to_uppercase()
#     )
#     .filter(pl.col("spec_type_desc").str.contains("BLOOD"))
#     .collect()
# )

# print(blood_cultures.shape)


## heatmap of the top 10 most common specimen types

query = (
    lazy_df
    .with_columns(
        pl.col("spec_type_desc").str.strip_chars().str.to_uppercase()
    )
    .group_by("spec_type_desc")
    .agg(pl.count())
    .sort("count", descending=True)
    .head(10)
)

specimen_counts = query.collect()

plt.figure(figsize=(10, 6))
sns.heatmap(specimen_counts.to_pandas().set_index("spec_type_desc"), annot=True, fmt="d", cmap="YlGnBu")
plt.title("Top 10 Most Common Specimen Types")
plt.savefig("../Figures/top_10_specimen_types.png")


# top 10 bacteria
query = (
    lazy_df
    .with_columns(
        pl.col("org_name").str.strip_chars().str.to_uppercase()
    )
    .group_by("org_name")
    .agg(pl.count())
    .sort("count", descending=True)
    .head(10)
)

bacteria_counts = query.collect()
plt.figure(figsize=(10, 6))
sns.heatmap(bacteria_counts.to_pandas().set_index("org_name"), annot=True, fmt="d", cmap="YlGnBu")
plt.title("Top 10 Most Common Bacteria")
plt.savefig("../Figures/top_10_bacteria.png")
