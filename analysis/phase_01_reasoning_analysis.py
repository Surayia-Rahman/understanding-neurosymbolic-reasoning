# phase_01_reasoning_analysis.py
# purpose: analyze reasoning performance of symbolic engine (v1)

import pandas as pd
from symbolic.graph_builder_v1 import TaxonomyGraphV1
from symbolic.path_finder_v1 import PathFinderV1

from analysis.experiment_logger_v1 import ExperimentLoggerV1

class ReasoningAnalyzerV1:
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.results = []

        # build graph
        self.graph_builder = TaxonomyGraphV1(csv_path)
        self.graph_builder.load_data()
        self.graph_builder.build_graph()

        self.path_finder = PathFinderV1(self.graph_builder.get_graph())

    def run_batch(self, queries):
        """
        queries: list of (source, target)
        """
        for source, target in queries:
            result = self.path_finder.reason(source, target)

            self.results.append({
                "source": source,
                "target": target,
                "answer": result["answer"],
                "reasoning_path": result["reasoning_path"],
                "hops": result["hops"]
            })

    def to_dataframe(self):
        return pd.DataFrame(self.results)

    def compute_metrics(self):
        df = self.to_dataframe()

        total = len(df)
        positive = len(df[df["answer"] == "yes"])
        negative = total - positive

        avg_hops = df["hops"].mean()

        path_exists_rate = len(df[df["reasoning_path"].notnull()]) / total

        return {
            "total_queries": total,
            "positive_answers": positive,
            "negative_answers": negative,
            "avg_hops": avg_hops,
            "path_found_rate": path_exists_rate
        }


if __name__ == "__main__":
    csv_path = "data/raw/taxonomy_v1.csv"

    analyzer = ReasoningAnalyzerV1(csv_path)

    queries = [
        ("cat", "living_thing"),
        ("rose", "animal"),
        ("sparrow", "living_thing"),
        ("shark", "animal"),
        ("dog", "animal"),
        ("tulip", "plant"),
        ("snake", "living_thing"),
        ("eagle", "plant")
    ]

    analyzer.run_batch(queries)

    df = analyzer.to_dataframe()
    print("\n=== RAW RESULTS ===")
    print(df)

    metrics = analyzer.compute_metrics()

    print("\n=== METRICS ===")
    for k, v in metrics.items():
        print(f"{k}: {v}")

    # save results

    logger = ExperimentLoggerV1()
    saved_df = logger.log_batch(
        analyzer.results,
        experiment_id="phase_01_batch_01"
    )

    print("\n=== saved to dataset ===")
    print(saved_df.tail())