# phase_02_path_deviation_analysis_v1.py
# purpose: compare clean and noisy reasoning paths

import pandas as pd


class PathDeviationAnalyzerV1:

    def __init__(self):

        self.clean = pd.read_csv(
            "results/phase_01_taxonomy/results.csv"
        )

        self.noisy = pd.read_csv(
            "results/phase_02_noisy_graph/results.csv"
        )

    def merge_results(self):

        merged = pd.merge(
            self.clean,
            self.noisy,
            on=["source", "target"],
            suffixes=("_clean", "_noisy")
        )

        return merged

    def analyze(self):

        df = self.merge_results()

        df["path_changed"] = (
            df["reasoning_path_clean"]
            !=
            df["reasoning_path_noisy"]
        )

        df["hop_difference"] = (
            df["hops_clean"]
            -
            df["hops_noisy"]
        )

        df["success_to_failure"] = (
            (df["answer_clean"] == "yes")
            &
            (df["answer_noisy"] == "no")
        )

        df["hallucinated_shortcut"] = (
            (df["answer_clean"] == "yes")
            &
            (df["answer_noisy"] == "yes")
            &
            (df["hop_difference"] > 0)
        )

        return df

    def summary(self, df):

        return {
            "total_queries": len(df),

            "path_change_rate":
                df["path_changed"].mean(),

            "success_to_failure_rate":
                df["success_to_failure"].mean(),

            "hallucinated_shortcuts":
                int(df["hallucinated_shortcut"].sum()),

            "avg_hop_difference":
                df["hop_difference"].mean()
        }

    def run_all(self):

        df = self.analyze()

        print("\n=== path deviation table ===")

        print(
            df[
                [
                    "source",
                    "target",
                    "path_changed",
                    "hop_difference",
                    "success_to_failure",
                    "hallucinated_shortcut"
                ]
            ]
        )

        print("\n=== summary ===")
        print(self.summary(df))


if __name__ == "__main__":

    analyzer = PathDeviationAnalyzerV1()

    analyzer.run_all()
    
"""
=== path deviation table ===
    source        target  ...  success_to_failure  hallucinated_shortcut
0      cat  living_thing  ...               False                   True
1     rose        animal  ...               False                  False
2  sparrow  living_thing  ...               False                  False
3    shark        animal  ...               False                  False
4      dog        animal  ...                True                  False
5    tulip         plant  ...               False                  False
6    snake  living_thing  ...               False                  False
7    eagle         plant  ...               False                  False

[8 rows x 6 columns]

=== summary ===
{'total_queries': 8, 'path_change_rate': np.float64(0.5), 'success_to_failure_rate': np.float64(0.125), 'hallucinated_shortcuts': 1, 'avg_hop_difference': np.float64(0.5)}"""