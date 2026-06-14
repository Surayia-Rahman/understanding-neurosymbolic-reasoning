# phase_02_robustness_report_v1.py
# purpose: generate statistical + visual robustness report

import pandas as pd
import matplotlib.pyplot as plt


class RobustnessReportV1:

    def __init__(self):

        self.df = pd.read_csv(
            "results/phase_02_noisy_graph/robustness_experiments.csv"
        )

    # 1. seed-level summary
    def seed_summary(self):

        grouped = self.df.groupby("seed")

        summary = grouped.agg({
            "hops": "mean",
            "answer": lambda x: (x == "yes").mean()
        }).rename(columns={
            "hops": "avg_hops",
            "answer": "success_rate"
        })

        return summary

    # 2. classification of seeds
    def classify_seeds(self, summary_df):

        def label(row):

            if row["success_rate"] >= 0.6:
                return "stable"

            elif row["success_rate"] >= 0.3:
                return "degraded"

            else:
                return "collapsed"

        summary_df["regime"] = summary_df.apply(label, axis=1)

        return summary_df

    # 3. visualization
    def plot_success_rate(self, summary_df):

        plt.figure(figsize=(8, 5))

        summary_df["success_rate"].plot(
            kind="bar"
        )

        plt.title("Phase 02 Robustness: Success Rate per Seed")
        plt.ylabel("Success Rate")

        output = "results/phase_02_noisy_graph/figures/success_rate_by_seed.png"

        plt.tight_layout()
        plt.savefig(output)

        print(f"saved: {output}")

    # 4. hop distribution plot
    def plot_hops(self):

        plt.figure(figsize=(8, 5))

        self.df["hops"].plot(
            kind="hist",
            bins=10
        )

        plt.title("Hop Distribution (Noisy Graph)")

        output = "results/phase_02_noisy_graph/figures/hop_distribution.png"

        plt.tight_layout()
        plt.savefig(output)

        print(f"saved: {output}")

    # -----------------------------
    # 5. markdown report
    # -----------------------------
    def save_report(self, summary_df):

        report = []

        report.append("# Phase 02 Robustness Report\n")

        report.append("## Seed-level summary\n")
        report.append(summary_df.to_string())
        report.append("\n")

        report.append("## Regime distribution\n")
        report.append(str(summary_df["regime"].value_counts()))
        report.append("\n")

        report.append("## Key findings\n")

        report.append(
            "- reasoning stability varies significantly across graph perturbations"
        )

        report.append(
            "- some seeds collapse completely (0% success rate)"
        )

        report.append(
            "- hop distributions shift toward shorter paths under noise"
        )

        output = "results/phase_02_noisy_graph/robustness_report.md"

        with open(output, "w", encoding="utf-8") as f:
            f.write("\n".join(report))

        print(f"saved: {output}")

    # run pipeline
    def run(self):

        summary = self.seed_summary()
        summary = self.classify_seeds(summary)

        print("\n=== seed summary ===")
        print(summary)

        print("\n=== regime counts ===")
        print(summary["regime"].value_counts())

        self.plot_success_rate(summary)
        self.plot_hops()
        self.save_report(summary)


if __name__ == "__main__":

    report = RobustnessReportV1()
    report.run()

"""
=== seed summary ===
      avg_hops  success_rate     regime
seed                                   
1        1.125         0.500   degraded
2        1.625         0.625     stable
3        1.500         0.625     stable
4        0.625         0.375   degraded
5        1.250         0.500   degraded
6        0.750         0.375   degraded
7        0.875         0.375   degraded
8        0.500         0.250  collapsed
9        0.000         0.000  collapsed
10       1.625         0.750     stable

=== regime counts ===
regime
degraded     5
stable       3
collapsed    2
Name: count, dtype: int64
saved: results/phase_02_noisy_graph/figures/success_rate_by_seed.png
saved: results/phase_02_noisy_graph/figures/hop_distribution.png
saved: results/phase_02_noisy_graph/robustness_report.md"""
