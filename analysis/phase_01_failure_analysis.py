# phase_01_failure_analysis.py
# purpose: diagnose reasoning failures in symbolic graph system

import pandas as pd


class FailureAnalyzerV1:
    def __init__(self, path="results/phase_01_taxonomy/results.csv"):
        self.df = pd.read_csv(path)

    def failure_rate(self):
        total = len(self.df)
        failures = self.df[self.df["answer"] == "no"]

        return {
            "total_queries": total,
            "failures": len(failures),
            "failure_rate": len(failures) / total
        }

    def unreachable_vs_wrong_target(self):
        unreachable = self.df[self.df["reasoning_path"].isna()]
        wrong_but_reachable = self.df[
            (self.df["answer"] == "no") &
            (self.df["reasoning_path"].notna())
        ]

        return {
            "unreachable_cases": len(unreachable),
            "reachable_but_wrong": len(wrong_but_reachable)
        }

    def hop_correlation(self):
        grouped = self.df.groupby("answer")["hops"].mean()

        return {
            "avg_hops_yes": float(grouped.get("yes", 0)),
            "avg_hops_no": float(grouped.get("no", 0))
        }

    def hardest_queries(self):
        # longest reasoning paths = most complex
        return self.df.sort_values(
            by="hops",
            ascending=False
        )[["source", "target", "answer", "hops"]].head(5)

    def run_all(self):
        print("\n=== failure rate ===")
        print(self.failure_rate())

        print("\n=== failure type ===")
        print(self.unreachable_vs_wrong_target())

        print("\n=== hop correlation ===")
        print(self.hop_correlation())

        print("\n=== hardest queriesS (by hops) ===")
        print(self.hardest_queries())


if __name__ == "__main__":
    analyzer = FailureAnalyzerV1()
    analyzer.run_all()