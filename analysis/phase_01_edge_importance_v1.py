# phase_01_edge_importance_v1.py
# purpose: compute edge-level importance in reasoning graph

import pandas as pd


class EdgeImportanceV1:

    def __init__(self,
                 path="results/phase_01_taxonomy/results.csv"):

        self.df = pd.read_csv(path)

    def extract_edges(self, row):

        if pd.isna(row["reasoning_path"]) or row["reasoning_path"] == "":
            return []

        nodes = [x.strip() for x in row["reasoning_path"].split("->")]

        edges = []
        for i in range(len(nodes) - 1):
            edges.append((nodes[i], nodes[i + 1]))

        return edges

    def build_edge_table(self):

        records = []

        for _, row in self.df.iterrows():

            edges = self.extract_edges(row)

            for (src, dst) in edges:

                records.append({
                    "edge": f"{src}->{dst}",
                    "source": row["source"],
                    "answer": row["answer"]
                })

        return pd.DataFrame(records)

    def compute_edge_stats(self):

        edges_df = self.build_edge_table()

        if edges_df.empty:
            return pd.DataFrame()

        grouped = edges_df.groupby("edge")

        stats = grouped["answer"].apply(list).reset_index()

        stats["total"] = stats["answer"].apply(len)
        stats["success"] = stats["answer"].apply(lambda x: x.count("yes"))
        stats["failure"] = stats["answer"].apply(lambda x: x.count("no"))

        stats["success_rate"] = stats["success"] / stats["total"]

        return stats.sort_values(
            by=["success_rate", "total"],
            ascending=[False, False]
        )

    def critical_edges(self):

        stats = self.compute_edge_stats()

        # edges that are both frequent and highly successful
        return stats[
            (stats["total"] >= 2) &
            (stats["success_rate"] >= 0.7)
        ]

    def run_all(self):

        print("\n=== edge importance table ===")
        print(self.compute_edge_stats())

        print("\n=== critical edge ===")
        print(self.critical_edges())


if __name__ == "__main__":
    analyzer = EdgeImportanceV1()
    analyzer.run_all()
    
"""
=== edge importance table ===
                    edge           answer  ...  failure  success_rate
0   animal->living_thing  [yes, yes, yes]  ...        0           1.0
6         mammal->animal       [yes, yes]  ...        0           1.0
1           bird->animal            [yes]  ...        0           1.0
2            cat->mammal            [yes]  ...        0           1.0
3            dog->mammal            [yes]  ...        0           1.0
4           fish->animal            [yes]  ...        0           1.0
5          flower->plant            [yes]  ...        0           1.0
7        reptile->animal            [yes]  ...        0           1.0
8            shark->fish            [yes]  ...        0           1.0
9         snake->reptile            [yes]  ...        0           1.0
10         sparrow->bird            [yes]  ...        0           1.0
11         tulip->flower            [yes]  ...        0           1.0

[12 rows x 6 columns]

=== critical edge ===
                   edge           answer  ...  failure  success_rate
0  animal->living_thing  [yes, yes, yes]  ...        0           1.0
6        mammal->animal       [yes, yes]  ...        0           1.0

[2 rows x 6 columns]"""
