
import pandas as pd


INPUT_CSV = "data/micro_events.csv"
OUTPUT_CSV = "data/micro_events_dedup.csv"

df = pd.read_csv(INPUT_CSV, low_memory=False)

df["event_dt"] = pd.to_datetime(df["charttime"], errors="coerce")
df["event_dt"] = df["event_dt"].fillna(pd.to_datetime(df["chartdate"], errors="coerce"))
df["year"] = df["event_dt"].dt.year

df = df.sort_values("event_dt")
df_dedup = df.drop_duplicates(subset=["subject_id", "org_name", "year"], keep="first")

df_dedup = df_dedup.drop(columns=["event_dt", "year"])
df_dedup.to_csv(OUTPUT_CSV, index=False)

print(f"Input rows: {len(df):,}")
print(f"Output rows: {len(df_dedup):,}")
print(f"Wrote: {OUTPUT_CSV}")