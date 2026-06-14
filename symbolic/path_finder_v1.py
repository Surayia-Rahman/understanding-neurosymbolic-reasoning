# path_finder_v1.py
# purpose: perform symbolic reasoning using graph traversal (v1)

import networkx as nx


class PathFinderV1:
    def __init__(self, graph):
        self.graph = graph

    def find_path(self, source, target):
        """
        returns shortest path if exists, else None
        """
        try:
            path = nx.shortest_path(self.graph, source=source, target=target)
            return path
        except nx.NetworkXNoPath:
            return None
        except nx.NodeNotFound:
            return None

    def reason(self, source, target):
        """
        returns symbolic reasoning result
        """
        path = self.find_path(source, target)

        if path is None:
            return {
                "answer": "no",
                "reasoning_path": None,
                "hops": 0
            }

        return {
            "answer": "yes",
            "reasoning_path": " -> ".join(path),
            "hops": len(path) - 1
        }


if __name__ == "__main__":
    # quick test (manual sanity check)

    import pandas as pd
    import networkx as nx

    # rebuild graph (same as v1 builder)
    df = pd.read_csv("data/raw/taxonomy_v1.csv")

    G = nx.DiGraph()
    for _, row in df.iterrows():
        G.add_edge(row["source"], row["target"], relation=row["relation"])

    pf = PathFinderV1(G)

    # test queries
    tests = [
        ("cat", "living_thing"),
        ("rose", "animal"),
        ("sparrow", "living_thing"),
        ("shark", "animal")
    ]

    for s, t in tests:
        result = pf.reason(s, t)
        print(f"{s} -> {t}")
        print(result)
        print("-" * 40)