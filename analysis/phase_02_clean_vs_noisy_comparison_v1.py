# phase_02_clean_vs_noisy_comparison_v1.py
# purpose: compare reasoning performance under clean vs noisy graph conditions

import pandas as pd
from symbolic.graph_builder_v1 import TaxonomyGraphV1
from analysis.phase_02_noisy_graph_generator_v1 import NoisyGraphGeneratorV1


class CleanVsNoisyEvaluatorV1:

    def __init__(self,
                 csv_path="data/raw/taxonomy_v1.csv",
                 results_path="results/phase_01_taxonomy/results.csv"):

        self.results = pd.read_csv(results_path)

        # clean graph
        builder = TaxonomyGraphV1(csv_path)
        builder.load_data()
        builder.build_graph()
        self.clean_graph = builder.get_graph()

        # noisy graph structure (simulated)
        self.noise_gen = NoisyGraphGeneratorV1(csv_path)
        self.noise = self.noise_gen.generate_noisy_graph()

    def simulate_noisy_failure(self, row):
        """
        heuristic: noisy environment increases failure probability
        """

        base_failure = 0.0

        # missing edges reduce success
        if row["hops"] >= 3:
            base_failure += 0.2

        # deeper reasoning is more fragile under noise
        if row["answer"] == "yes":
            base_failure += 0.1

        # simulate corruption pressure
        if len(self.noise["corrupted_edges"]) > 15:
            base_failure += 0.15

        return min(1.0, base_failure)

    def evaluate(self):

        df = self.results.copy()

        # clean success (ground truth)
        df["clean_success"] = df["answer"].apply(lambda x: 1 if x == "yes" else 0)

        # noisy success (simulated degradation)
        df["noise_failure_prob"] = df.apply(self.simulate_noisy_failure, axis=1)
        df["noisy_success"] = 1 - df["noise_failure_prob"]

        return df

    def summary(self, df):

        return {
            "clean_avg_success": df["clean_success"].mean(),
            "noisy_avg_success": df["noisy_success"].mean(),
            "robustness_drop": df["clean_success"].mean() - df["noisy_success"].mean(),
            "avg_noise_failure": df["noise_failure_prob"].mean()
        }

    def run_all(self):

        df = self.evaluate()

        print("\n=== clean vs noisy reasoning ===")

        print(df[[
            "source",
            "target",
            "answer",
            "hops",
            "clean_success",
            "noisy_success",
            "noise_failure_prob"
        ]])

        print("\n=== summary ===")
        print(self.summary(df))


if __name__ == "__main__":
    evaluator = CleanVsNoisyEvaluatorV1()
    evaluator.run_all()