# phase_01_graph_failure_heatmap.py
# purpose: identify weak nodes in the knowledge graph

from asyncio.log import logger

import pandas as pd
from analysis.graph_vulnerability_logger_v1 import GraphVulnerabilityLoggerV1


class GraphFailureHeatmapV1:
    def __init__(self,
                 results_path="results/phase_01_taxonomy/results.csv"):

        self.df = pd.read_csv(results_path)

    def node_failure_score(self):
        failures = self.df[self.df["answer"] == "no"]

        score = failures["source"].value_counts().reset_index()
        score.columns = ["node", "failure_count"]

        return score

    def node_success_score(self):
        success = self.df[self.df["answer"] == "yes"]

        score = success["source"].value_counts().reset_index()
        score.columns = ["node", "success_count"]

        return score

    def merge_scores(self):
        fail = self.node_failure_score()
        success = self.node_success_score()

        merged = pd.merge(
            success,
            fail,
            on="node",
            how="outer"
        ).fillna(0)

        merged["total"] = merged["success_count"] + merged["failure_count"]
        merged["failure_rate"] = merged["failure_count"] / merged["total"]

        return merged.sort_values(
            by="failure_rate",
            ascending=False
        )

    def run_all(self):

        merged = self.merge_scores()

        print("\n=== node vulnerability rank ===")
        print(merged)

        logger = GraphVulnerabilityLoggerV1()
        logger.save(merged)
        


if __name__ == "__main__":
    analyzer = GraphFailureHeatmapV1()
    analyzer.run_all()