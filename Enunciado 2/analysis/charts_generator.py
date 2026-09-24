#!/usr/bin/env python3
"""Generate analytical charts from the consolidated experiment outputs."""

from charts.loaders import load_analysis_summary, load_monte_carlo, load_quality, load_trials
from charts.monte_carlo import plot_monte_carlo
from charts.rq1 import plot_time_by_kata, plot_time_difference
from charts.rq2 import plot_attempts, plot_success_rate
from charts.rq3 import plot_quality_distributions, plot_quality_effects, plot_quality_radar


def main() -> None:
    trials_df = load_trials()
    quality_df = load_quality()
    summaries = load_analysis_summary()
    simulations = load_monte_carlo()

    print("Gerando gráficos analíticos...")
    plot_time_by_kata(trials_df)
    plot_time_difference(trials_df)
    plot_attempts(trials_df)
    plot_success_rate(trials_df)
    valid_quality = quality_df.merge(
        trials_df[["developer", "kata_key", "treatment", "success", "timeout"]],
        on=["developer", "kata_key", "treatment"],
        how="left",
    )
    valid_quality = valid_quality[valid_quality["success"] & ~valid_quality["timeout"]].copy()
    plot_quality_distributions(quality_df, trials_df)
    plot_quality_radar(valid_quality)
    plot_quality_effects(valid_quality)
    stats_summary = summaries.get("stats_summary.json")
    if simulations is not None and stats_summary is not None:
        plot_monte_carlo(simulations, stats_summary)
    print("Gráficos gravados em analysis/output/charts")


if __name__ == "__main__":
    main()
