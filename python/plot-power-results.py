import pandas as pd
import matplotlib.pyplot as plt

def make_power_plot(csv_path: str = "power-results.csv", output_path: str = "power-plot.png"):
    df = pd.read_csv(csv_path)
    
    dist_order = ["Normal", "Right-skewed", "Heavy-tailed", "Uniform"]
    n_order = [20, 50, 100]
    test_order = ["Welch t-test", "Wilcoxon Rank-Sum Test"]
    
    color_map = {
        20: "#D55E00",
        50: "#0072B2",
        100: "#009E73"
    }
    
    linestyle_map = {
        "Welch t-test": "--",
        "Wilcoxon Rank-Sum Test": "-"
    }
    
    fig, axes = plt.subplots(2, 2, figsize = (10, 7), sharex = True, sharey = True)
    axes = axes.flatten()
    
    for ax, dist in zip(axes, dist_order):
        subset = df[df["dist"] == dist]
        
        for n in n_order:
            for test in test_order:
                temp = subset[(subset["n"] == n) & (subset["test"] == test)].sort_values("delta")
                ax.plot(
                    temp["delta"],
                    temp["power"],
                    label = f"n = {n}, {test}",
                    color = color_map[n],
                    linestyle = linestyle_map[test],
                    marker = "o",
                    linewidth = 1.4,
                    markersize = 4
                )
        
        ax.set_title(dist, fontweight = "bold")
        ax.set_xlabel("Effect Size")
        ax.set_ylabel("Empirical Power")
        ax.set_ylim(0, 1.05)
        
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc = "lower center", ncol = 3, frameon = False)
    fig.suptitle("Empirical Power Comparison")
    fig.tight_layout(rect = [0, 0.08, 1, 0.95])
    
    plt.savefig(output_path, dpi = 300, bbox_inches = "tight")
    plt.close()
    print(f"Saved plot to {output_path}")
    
if __name__ == "__main__":
    make_power_plot()
