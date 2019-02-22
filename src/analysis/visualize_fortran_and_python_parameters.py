from bld.project_paths import project_paths_join as ppj
import pandas as pd
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns
import sys

sns.set_style("white")


def plot_results_comparison(df, colnames, path, title):
    # abbreviations
    nr_cols = len(colnames)
    nr_rows = len(df)
    y_max = nr_rows * (nr_cols + 1)

    # plot settings
    colors = [
        "royalblue",
        "firebrick",
        "seagreen",
        "orange",
        "black",
        "darkslateblue",
        "r",
        "khaki",
    ]

    fig, ax = plt.subplots(figsize=(7, 0.5 * nr_rows))
    axes = {}

    for i, col in enumerate(colnames):
        axes[col] = ax.barh(
            bottom=i + np.array(range(0, y_max, (nr_cols + 1))),
            width=df[col],
            height=0.9,
            color=colors[i],
            alpha=0.9,
        )

    ax.locator_params(axis="x", nbins=4)
    ax.set_yticks(0.5 * nr_cols + np.array(range(0, y_max, (nr_cols + 1))))
    ax.set_yticklabels(df.index)

    ax.tick_params(axis="both", which="major", labelsize=22)

    ax.xaxis.tick_top()

    ax.axvline(x=0.0, ymin=0, ymax=y_max, linewidth=1.0, color="k")

    ax.set_ylim(0, y_max)
    ax.set_autoscale_on(False)

    ax.legend([axes[col] for col in colnames], colnames, fontsize=14)

    plt.title(
        title, fontsize=28, y=1 + 2.5 / nr_rows, x=-0.6, loc="left", weight="bold"
    )

    plt.savefig(path, bbox_inches="tight", pad_inches=0.8)
    plt.close(fig)


if __name__ == "__main__":
    model, dataset = sys.argv[1:3]
    true_path = ppj("LIBRARY", "true_{}_results.csv")
    true_df = pd.read_csv(true_path.format(model), index_col="index")
    estimated_path = ppj("OUT_ANALYSIS", "{}_{}/results_df.csv")
    estimated_df = pd.read_csv(estimated_path.format(model, dataset), index_col="index")
    df = pd.concat([estimated_df, true_df], axis=1)

    df["Fortran"] = df["chs_params"] - df["true_value"]
    df["Python"] = df["params"] - df["true_value"]

    plot_results_comparison(
        df=df,
        colnames=["Python", "Fortran"],
        path=ppj("OUT_ANALYSIS", "{}_{}/comparison_plot".format(model, dataset)),
        title=(
            "Comparison of Python and Fortran results\nBars show "
            "deviation from true population Parameters"
        ),
    )
