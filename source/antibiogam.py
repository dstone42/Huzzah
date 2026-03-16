import polars as pl
import matplotlib.pyplot as plt
import seaborn as sns

# load the data from data/micro_events.csv
lazy_df = pl.scan_csv("../data/micro_events.csv")

blood_culture_lazy = lazy_df.filter(
    pl.col("spec_type_desc").str.contains("(?i)blood")
)

unique_orgs = (
    blood_culture_lazy
    .select("org_name")
    .unique()
    .collect()
    .get_column("org_name")
    .to_list()
)


sensitivity_stats = (
    blood_culture_lazy
    .filter(pl.col("org_name").is_not_null() & pl.col("ab_name").is_not_null())
    .filter(pl.col("interpretation").is_not_null())
    .group_by(["ab_name", "org_name"])
    .agg(
        # Mean of a boolean gives the percentage (0.0 to 1.0)
        # Multiplying by 100 to get 0-100 range
        ((pl.col("interpretation").str.to_uppercase() == "S").mean() * 100).round(1).alias("pct_sensitive")
    )
)


antibiogram = (
    sensitivity_stats.collect()
    .pivot(
        on="org_name",
        index="ab_name",
        values="pct_sensitive"
    )
    .sort("ab_name")
)

print(antibiogram)
antibiogram.write_csv("antibiogram_check.csv")