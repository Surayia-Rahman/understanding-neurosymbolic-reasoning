# phase_03_failure_analysis_v1.py
# purpose: analyze TF-IDF retrieval failure modes 

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


class Phase03FailureAnalyzerV1:

    def __init__(self,
                 results_path="results/phase_03_embeddings/retrieval_results_v1.csv"):

        self.results_path = results_path
        self.df = None


    def load_data(self):
        self.df = pd.read_csv(self.results_path)


    def compute_metrics(self):

        total = len(self.df)
        correct = self.df["correct"].sum()
        accuracy = correct / total

        avg_sim = self.df["similarity"].mean()

        return {
            "total_samples": total,
            "accuracy": accuracy,
            "avg_similarity": avg_sim
        }

    # Failure categorization
    def categorize_failures(self):

        def classify(row):

            if row["correct"]:
                return "correct"

            if row["similarity"] == 0:
                return "lexical_mismatch_failure"

            if row["similarity"] < 0.3:
                return "weak_retrieval_failure"

            return "misclassification"

        self.df["failure_type"] = self.df.apply(classify, axis=1)

        return self.df

    # Failure summary-
    def failure_summary(self):

        summary = self.df["failure_type"].value_counts().to_dict()
        return summary

    # Hardest queries
    def hardest_cases(self):

        return self.df.sort_values("similarity").head(5)

    def plot_similarity_distribution(self):

        output_dir = "results/phase_03_embeddings/figures"
        os.makedirs(output_dir, exist_ok=True)

        plt.figure()

        plt.hist(self.df["similarity"], bins=10)
        plt.title("TF-IDF Similarity Distribution (Phase 03)")
        plt.xlabel("cosine similarity")
        plt.ylabel("frequency")

        path = os.path.join(output_dir, "similarity_distribution_v1.png")
        plt.savefig(path, bbox_inches="tight")

        print(f"\nsaved: {path}")

    def run(self):

        self.load_data()
        self.categorize_failures()

        print("\n=== BASIC METRICS ===")
        print(self.compute_metrics())

        print("\n=== FAILURE BREAKDOWN ===")
        print(self.failure_summary())

        print("\n=== HARDEST CASES ===")
        print(self.hardest_cases()[["query", "expected", "predicted", "similarity"]])

        self.plot_similarity_distribution()

        # save enriched results
        output_dir = "results/phase_03_embeddings"
        os.makedirs(output_dir, exist_ok=True)

        out_path = os.path.join(output_dir, "retrieval_results_with_failures.csv")
        self.df.to_csv(out_path, index=False)

        print(f"\nsaved: {out_path}")


if __name__ == "__main__":

    analyzer = Phase03FailureAnalyzerV1()
    analyzer.run()
    
"""
=== BASIC METRICS ===
{'total_samples': 10, 'accuracy': np.float64(0.1), 'avg_similarity': np.float64(0.0)}

=== FAILURE BREAKDOWN ===
{'lexical_mismatch_failure': 9, 'correct': 1}

=== HARDEST CASES ===
    query expected predicted  similarity
0  kitten      cat     whale         0.0
1   puppy      dog     whale         0.0
2    orca    whale     whale         0.0
3  canary  sparrow     whale         0.0
4    hawk    eagle     whale         0.0

saved: results/phase_03_embeddings/figures\similarity_distribution_v1.png

saved: results/phase_03_embeddings\retrieval_results_with_failures.csv"""
