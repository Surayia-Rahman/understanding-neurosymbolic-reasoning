# noisy_path_finder_v1.py
# purpose: perform reasoning on a physically corrupted graph

import networkx as nx

from phase_02.symbolic.noisy_graph_builder_v1 import (
    NoisyGraphBuilderV1
)


class NoisyPathFinderV1:

    def __init__(self):

        builder = NoisyGraphBuilderV1()

        self.graph = builder.create_noisy_graph()

    def query(self, source, target):

        try:

            path = nx.shortest_path(
                self.graph,
                source=source,
                target=target
            )

            return {
                "answer": "yes",
                "reasoning_path": " -> ".join(path),
                "hops": len(path) - 1
            }

        except nx.NetworkXNoPath:

            return {
                "answer": "no",
                "reasoning_path": None,
                "hops": 0
            }

    def run_demo(self):

        test_queries = [

            ("cat", "living_thing"),
            ("rose", "animal"),
            ("sparrow", "living_thing"),
            ("shark", "animal"),
            ("dog", "animal"),
            ("tulip", "plant"),
            ("snake", "living_thing"),
            ("eagle", "plant")
        ]

        for source, target in test_queries:

            print("\n" + "-" * 50)

            print(
                f"{source} -> {target}"
            )

            print(
                self.query(
                    source,
                    target
                )
            )


if __name__ == "__main__":

    finder = NoisyPathFinderV1()

    finder.run_demo()
    
"""--------------------------------------------------
cat -> living_thing
{'answer': 'yes', 'reasoning_path': 'cat -> living_thing', 'hops': 1}

--------------------------------------------------
rose -> animal
{'answer': 'no', 'reasoning_path': None, 'hops': 0}

--------------------------------------------------
sparrow -> living_thing
{'answer': 'yes', 'reasoning_path': 'sparrow -> bird -> animal -> living_thing', 'hops': 3}

--------------------------------------------------
shark -> animal
{'answer': 'yes', 'reasoning_path': 'shark -> fish -> animal', 'hops': 2}

--------------------------------------------------
dog -> animal
{'answer': 'no', 'reasoning_path': None, 'hops': 0}

--------------------------------------------------
tulip -> plant
{'answer': 'yes', 'reasoning_path': 'tulip -> flower -> plant', 'hops': 2}

--------------------------------------------------
snake -> living_thing
{'answer': 'yes', 'reasoning_path': 'snake -> reptile -> animal -> living_thing', 'hops': 3}

--------------------------------------------------
eagle -> plant
{'answer': 'no', 'reasoning_path': None, 'hops': 0}"""
