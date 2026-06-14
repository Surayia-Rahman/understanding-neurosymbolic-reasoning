# phase_01_path_explainability.py
# purpose: score reasoning paths for explainability quality

import pandas as pd


class PathExplainabilityV1:

    def __init__(self,
                 path="results/phase_01_taxonomy/results.csv"):

        self.df = pd.read_csv(path)

    def compute_score(self, row):
        """
        simple heuristic scoring function
        """

        # base score
        score = 0.5

        # reward successful reasoning
        if row["answer"] == "yes":
            score += 0.3

        # penalize missing paths
        if pd.isna(row["reasoning_path"]) or row["reasoning_path"] == "":
            score -= 0.4

        # small penalty for very long chains (noise risk)
        if row["hops"] > 3:
            score -= 0.1

        # reward moderate reasoning depth (signal)
        if 1 <= row["hops"] <= 3:
            score += 0.1

        return max(0.0, min(1.0, score))

    def score_all(self):

        df = self.df.copy()

        df["path_score"] = df.apply(self.compute_score, axis=1)

        return df[[
            "source",
            "target",
            "answer",
            "hops",
            "path_score"
        ]].sort_values(by="path_score", ascending=False)

    def summary(self):

        df = self.df.copy()
        df["path_score"] = df.apply(self.compute_score, axis=1)

        return {
            "avg_path_score": df["path_score"].mean(),
            "min_path_score": df["path_score"].min(),
            "max_path_score": df["path_score"].max()
        }

    def run_all(self):

        print("\n=== path explainability score ===")
        print(self.score_all())

        print("\n=== SUMMARY ===")
        print(self.summary())


if __name__ == "__main__":
    analyzer = PathExplainabilityV1()
    analyzer.run_all()