import os
import datetime

import pandas as pd
import matplotlib.pyplot as plt

project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
output_dir = os.path.join(project_root, "output")

df_dou = pd.DataFrame()
df_work_ua = pd.DataFrame()

dou_path = os.path.join(output_dir, "dou_vacancies.csv")
work_ua_path = os.path.join(output_dir, "work_ua_vacancies.csv")

if os.path.exists(dou_path):
    df_dou = pd.read_csv(dou_path)
    print(f"Loaded {len(df_dou)} vacancies from DOU")
else:
    print(f"Warning: File not found - {dou_path}")

if os.path.exists(work_ua_path):
    df_work_ua = pd.read_csv(work_ua_path)
    print(f"Loaded {len(df_work_ua)} vacancies from Work.ua")
else:
    print(f"Warning: File not found - {work_ua_path}")

df = pd.concat([df_dou, df_work_ua], ignore_index=True)

if len(df) == 0:
    print("No data found. Please run scrapers first to generate vacancy data.")
    exit()

current_date = datetime.datetime.now().strftime("%Y-%m-%d")
figures_dir = os.path.join(output_dir, "figures")
os.makedirs(figures_dir, exist_ok=True)

df["technologies"] = df["technologies"].apply(
    lambda x: x.split(',') if isinstance(x, str) else x
)

tech_counts = df["technologies"].explode().value_counts()
total_vacancies = len(df)
tech_percentage = tech_counts / total_vacancies * 100

plt.figure(figsize=(12, 8))
tech_counts.head(15).plot(kind="bar", color="skyblue")
plt.title("Most Popular Python Technologies in Job Listings by counts")
plt.xlabel("Technology")
plt.ylabel("Number of Vacancies")
plt.xticks(rotation=45, ha="right")
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.savefig(f"{figures_dir}/tech_counts_{current_date}.png")
print(f"Diagram saved in 'tech_counts_{current_date}.png'")

plt.figure(figsize=(12, 8))
tech_percentage.head(15).plot(kind="bar", color="skyblue")
plt.title("Most Popular Python Technologies in Job Listings by percentage")
plt.xlabel("Technology")
plt.ylabel("Percentage")
plt.xticks(rotation=45, ha="right")
plt.grid(axis="y", linestyle="--", alpha=0.7)
plt.tight_layout()
plt.savefig(f"{figures_dir}/tech_percentage_{current_date}.png")
print(f"Diagram saved in 'tech_percentage_{current_date}.png'")

print(f"Analyzing {len(df)} total vacancies")
