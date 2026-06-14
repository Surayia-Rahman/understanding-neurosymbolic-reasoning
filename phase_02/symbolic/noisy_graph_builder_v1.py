# noisy_graph_builder_v1.py
# purpose: create a physically corrupted graph for robustness experiments

import random
import networkx as nx

from symbolic.graph_builder_v1 import TaxonomyGraphV1


class NoisyGraphBuilderV1:

    def __init__(
        self,
        csv_path="data/raw/taxonomy_v1.csv"
    ):

        builder = TaxonomyGraphV1(csv_path)

        builder.load_data()
        builder.build_graph()

        self.clean_graph = builder.get_graph()

    def create_noisy_graph(
        self,
        edge_removal_rate=0.15,
        edge_corruption_rate=0.10,
        seed=42
    ):

        random.seed(seed)

        noisy_graph = self.clean_graph.copy()


        # remove valid edges
        original_edges = list(noisy_graph.edges())

        for edge in original_edges:

            if random.random() < edge_removal_rate:

                if noisy_graph.has_edge(*edge):
                    noisy_graph.remove_edge(*edge)

   
        # inject corrupted edges

        nodes = list(noisy_graph.nodes())

        num_corruptions = max(
            1,
            int(len(original_edges) * edge_corruption_rate)
        )

        for _ in range(num_corruptions):

            source = random.choice(nodes)
            target = random.choice(nodes)

            if source != target:

                noisy_graph.add_edge(
                    source,
                    target,
                    relation="corrupted_is_a"
                )

        return noisy_graph

    def graph_stats(self, graph):

        return {
            "nodes": graph.number_of_nodes(),
            "edges": graph.number_of_edges(),
            "density": nx.density(graph)
        }


if __name__ == "__main__":

    builder = NoisyGraphBuilderV1()

    noisy_graph = builder.create_noisy_graph()

    print("\n=== clean graph ===")
    print(
        builder.graph_stats(
            builder.clean_graph
        )
    )

    print("\n=== noisy graph ===")
    print(
        builder.graph_stats(
            noisy_graph
        )
    )
    
"""
=== clean graph ===
{'nodes': 20, 'edges': 19, 'density': 0.05}

=== noisy graph ===
{'nodes': 20, 'edges': 16, 'density': 0.042105263157894736}"""
