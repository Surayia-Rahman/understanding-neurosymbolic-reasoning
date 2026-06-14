# phase_02_noisy_graph_generator_v1.py
# purpose: generate controlled noisy versions of taxonomy graph

import pandas as pd
import random
from symbolic.graph_builder_v1 import TaxonomyGraphV1


class NoisyGraphGeneratorV1:

    def __init__(self,
                 csv_path="data/raw/taxonomy_v1.csv"):

        self.csv_path = csv_path

        builder = TaxonomyGraphV1(csv_path)
        builder.load_data()
        builder.build_graph()

        self.graph = builder.get_graph()

        self.edges = list(self.graph.edges(data=True))

    def remove_edges(self, drop_rate=0.2):

        """simulate missing knowledge"""

        kept = [
            e for e in self.edges
            if random.random() > drop_rate
        ]

        return kept

    def corrupt_edges(self, corrupt_rate=0.1):

        """inject incorrect symbolic relations"""

        corrupted = []

        nodes = list(self.graph.nodes())

        for src, dst, data in self.edges:

            if random.random() < corrupt_rate:

                new_dst = random.choice(nodes)

                corrupted.append((src, new_dst, {"relation": "is_a"}))
            else:
                corrupted.append((src, dst, data))

        return corrupted

    def generate_noisy_graph(self):

        removed = self.remove_edges(drop_rate=0.15)
        corrupted = self.corrupt_edges(corrupt_rate=0.1)

        return {
            "removed_edges": removed,
            "corrupted_edges": corrupted
        }

    def run_all(self):

        noise = self.generate_noisy_graph()

        print("\n=== noisy graph stats ===")
        print("removed edges:", len(noise["removed_edges"]))
        print("corrupted edges:", len(noise["corrupted_edges"]))


if __name__ == "__main__":
    gen = NoisyGraphGeneratorV1()
    gen.run_all()
    
"""
=== noisy graph stats ===
removed edges: 14
corrupted edges: 19"""
