# phase_01_graph_analysis.py
# purpose: analyze and visualize the taxonomy graph

import networkx as nx
import matplotlib.pyplot as plt

from symbolic.graph_builder_v1 import TaxonomyGraphV1
from analysis.graph_artifact_logger_v1 import GraphArtifactLoggerV1


class GraphAnalyzerV1:
    def __init__(self, csv_path):
        self.csv_path = csv_path

        builder = TaxonomyGraphV1(csv_path)
        builder.load_data()
        builder.build_graph()

        self.graph = builder.get_graph()

    def basic_stats(self):
        return {
            "nodes": self.graph.number_of_nodes(),
            "edges": self.graph.number_of_edges(),
            "density": nx.density(self.graph)
        }

    def degree_analysis(self):
        degrees = dict(self.graph.degree())

        sorted_degrees = sorted(
            degrees.items(),
            key=lambda x: x[1],
            reverse=True
        )

        return sorted_degrees[:10]

    def visualize_graph(self):
        plt.figure(figsize=(10, 8))

        pos = nx.spring_layout(
            self.graph,
            seed=42
        )

        nx.draw(
            self.graph,
            pos,
            with_labels=True
        )

        plt.title("phase 01 taxonomy graph")

        output_path = (
            "results/phase_01_taxonomy/"
            "figures/graph_visualization_v1.png"
        )

        plt.savefig(
            output_path,
            bbox_inches="tight"
        )

        print(
            f"\nfigure saved: {output_path}"
        )

        plt.show()


if __name__ == "__main__":

    analyzer = GraphAnalyzerV1(
        "data/raw/taxonomy_v1.csv"
    )

    print("\n=== basic graph stats ===")
    print(analyzer.basic_stats())

    print("\n=== top connected nodes ===")
    print(analyzer.degree_analysis())

    logger = GraphArtifactLoggerV1()

    logger.save_graph_metrics(
        analyzer.basic_stats()
    )

    logger.save_centrality(
        analyzer.degree_analysis()
    )

    analyzer.visualize_graph()