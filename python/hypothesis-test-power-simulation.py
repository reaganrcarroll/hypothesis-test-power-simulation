import numpy as np
import pandas as pd
from scipy.stats import ttest_ind, mannwhitneyu

def generate_samples(n: int, dist: str, delta: float, rng: np.random.Generator):
    """Generate two independent samples under the specified distribution."""
    if dist == "normal":
        x = rng.normal(loc = 0, scale = 1, size = n)
        y = rng.normal(loc = delta, scale = 1, size = n)
    
    elif dist == "exponential":
        x = rng.exponential(scale = 1, size = n)
        y = rng.exponential(scale = 1, size = n) + delta
        
    elif dist == "heavy":
        x = rng.standard_t(df = 3, size = n)
        y = rng.standard_t(df = 3, size = n) + delta
        
    elif dist == "uniform":
        x = rng.uniform(low = 0, high = 1, size = n)
        y = rng.uniform(low = 0, high = 1, size = n) + delta
        
    else:
        raise ValueError(f"Unknown distribution: {dist}")
        
    return x, y
    
def simulate_power(
    n: int,
    dist: str,
    delta: float,
    reps: int = 10000,
    alpha: float = 0.05,
    seed: int | None = None
) -> pd.DataFrame:
    """Estimated empirical power for Welch t-test and Wilcoxon rank-sum test."""
    rng = np.random.default_rng(seed)
    
    reject_t = 0
    reject_w = 0
    
    for _ in range(reps):
        x, y = generate_samples(n, dist, delta, rng)
        
        # Welch two-sample t-test
        t_p = ttest_ind(x, y, equal_var = False).pvalue
        if t_p < alpha:
            reject_t += 1
            
        # Wilcoxon rank-sum test
        w_p = mannwhitneyu(x, y, alternative = "two-sided").pvalue
        if w_p < alpha:
            reject_w += 1
            
    return pd.DataFrame({
    "dist": [dist, dist],
    "n": [n, n],
    "delta": [delta, delta],
    "test": ["Welch t-test", "Wilcoxon Rank-Sum Test"],
    "power": [reject_t / reps, reject_w / reps]
})

def run_full_simulation(
    ns = (20, 50, 100),
    deltas = (0, 0.2, 0.5, 1.0),
    dists = ("normal", "exponential", "heavy", "uniform"),
    reps: int = 10000,
    base_seed: int = 123
) -> pd.DataFrame:
    """Run the full simulation study across all settings."""
    results = []
    counter = 0
    
    for dist in dists:
        for n in ns:
            for delta in deltas:
                result = simulate_power(
                n = n,
                dist = dist,
                delta = delta,
                reps = reps,
                seed = base_seed + counter
                )
                results.append(result)
                counter += 1
                
    final_results = pd.concat(results, ignore_index = True)
    
    dist_labels = {
        "normal": "Normal",
        "exponential": "Right-skewed",
        "heavy": "Heavy-tailed",
        "uniform": "Uniform"
    }
    final_results["dist"] = final_results["dist"].map(dist_labels)
    
    return final_results
    
if __name__ == "__main__":
    results = run_full_simulation(reps = 10000)
    results.to_csv("power_results.csv", index = False)
    print(results.head())
    print("\nSaved results to power_results.csv")
    
