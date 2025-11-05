import argparse
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

REQUIRED_COLS = [
    "Diet_type",
    "Recipe_name",
    "Cuisine_type",
    "Protein(g)",
    "Carbs(g)",
    "Fat(g)",
]

def load_dataset(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    for col in REQUIRED_COLS:
        if col not in df.columns:
            raise ValueError(f"missing column: {col}")
    return df

def coerce_and_fill(df: pd.DataFrame) -> pd.DataFrame:
    for col in ["Protein(g)", "Carbs(g)", "Fat(g)"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df["Protein(g)"] = df["Protein(g)"].fillna(df["Protein(g)"].mean(skipna=True))
    df["Carbs(g)"] = df["Carbs(g)"].fillna(df["Carbs(g)"].mean(skipna=True))
    df["Fat(g)"] = df["Fat(g)"].fillna(df["Fat(g)"].mean(skipna=True))
    return df

def add_ratios(df: pd.DataFrame) -> pd.DataFrame:
    df["Protein_to_Carbs_ratio"] = np.where(
        df["Carbs(g)"] != 0, df["Protein(g)"] / df["Carbs(g)"], np.nan
    )
    df["Carbs_to_Fat_ratio"] = np.where(
        df["Fat(g)"] != 0, df["Carbs(g)"] / df["Fat(g)"], np.nan
    )
    return df

def calc_avg_macros(df: pd.DataFrame) -> pd.DataFrame:
    avg = (
        df.groupby("Diet_type")[["Protein(g)", "Carbs(g)", "Fat(g)"]]
        .mean()
        .sort_values("Protein(g)", ascending=False)
    )
    return avg

def top_n_by_protein(df: pd.DataFrame, n: int) -> pd.DataFrame:
    return (
        df.sort_values("Protein(g)", ascending=False)
        .groupby("Diet_type", group_keys=False)
        .head(n)
    )

def most_common_cuisine(df: pd.DataFrame) -> pd.DataFrame:
    s = df.groupby("Diet_type")["Cuisine_type"].agg(lambda x: x.value_counts().idxmax())
    return s.to_frame(name="Most_common_cuisine")

def highest_protein_summary(df: pd.DataFrame, avg_df: pd.DataFrame) -> pd.DataFrame:
    max_row = df.loc[df["Protein(g)"].idxmax()]
    max_single_diet = str(max_row["Diet_type"])
    max_single_val = float(max_row["Protein(g)"])
    max_avg_diet = avg_df.index[0]
    max_avg_val = float(avg_df.iloc[0]["Protein(g)"])
    return pd.DataFrame(
        [
            {
                "diet_with_highest_single_recipe_protein": max_single_diet,
                "highest_single_recipe_protein_g": max_single_val,
                "diet_with_highest_avg_protein": max_avg_diet,
                "highest_avg_protein_g": max_avg_val,
            }
        ]
    )

def plot_avg_macros(avg_df: pd.DataFrame, outdir: str) -> str:
    x = np.arange(len(avg_df.index))
    width = 0.25
    plt.figure(figsize=(10, 6))
    plt.bar(x - width, avg_df["Protein(g)"], width, label="Protein(g)")
    plt.bar(x, avg_df["Carbs(g)"], width, label="Carbs(g)")
    plt.bar(x + width, avg_df["Fat(g)"], width, label="Fat(g)")
    plt.xticks(x, avg_df.index, rotation=25, ha="right")
    plt.ylabel("grams")
    plt.title("Average Macronutrients by Diet Type")
    plt.legend()
    path = os.path.join(outdir, "01_bar_avg_macros.png")
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()
    return path

def plot_heatmap(avg_df: pd.DataFrame, outdir: str) -> str:
    data = avg_df[["Protein(g)", "Carbs(g)", "Fat(g)"]].to_numpy()
    plt.figure(figsize=(8, max(4, len(avg_df.index) * 0.35)))
    plt.imshow(data, aspect="auto")
    plt.colorbar(label="grams")
    plt.yticks(range(len(avg_df.index)), avg_df.index)
    plt.xticks(range(3), ["Protein(g)", "Carbs(g)", "Fat(g)"])
    plt.title("Heatmap: Average Macros by Diet Type")
    path = os.path.join(outdir, "02_heatmap_avg_macros.png")
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()
    return path

def plot_scatter_top(top_df: pd.DataFrame, outdir: str) -> str | None:
    if top_df.empty:
        return None
    plt.figure(figsize=(10, 6))
    for d, g in top_df.groupby("Diet_type"):
        plt.scatter(g["Carbs(g)"], g["Protein(g)"], label=d, alpha=0.7)
    plt.xlabel("Carbs (g)")
    plt.ylabel("Protein (g)")
    plt.title("Top Protein Recipes by Diet")
    plt.legend(fontsize=8)
    path = os.path.join(outdir, "03_scatter_top_protein.png")
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()
    return path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", default="All_Diets.csv")
    parser.add_argument("--out", default="outputs")
    parser.add_argument("--topn", type=int, default=5)
    args = parser.parse_args()

    os.makedirs(args.out, exist_ok=True)

    df = load_dataset(args.csv)
    df = coerce_and_fill(df)
    df = add_ratios(df)
    df.to_csv(os.path.join(args.out, "cleaned_dataset.csv"), index=False)

    avg_df = calc_avg_macros(df)
    avg_df.to_csv(os.path.join(args.out, "avg_macros_by_diet.csv"))

    top_df = top_n_by_protein(df, args.topn)
    top_df.to_csv(os.path.join(args.out, "top_protein_by_diet.csv"), index=False)

    mc_df = most_common_cuisine(df)
    mc_df.to_csv(os.path.join(args.out, "most_common_cuisine_by_diet.csv"))

    summary_df = highest_protein_summary(df, avg_df)
    summary_df.to_csv(os.path.join(args.out, "highest_protein_summary.csv"), index=False)

    plot_avg_macros(avg_df, args.out)
    plot_heatmap(avg_df, args.out)
    plot_scatter_top(top_df, args.out)

if __name__ == "__main__":
    main()
