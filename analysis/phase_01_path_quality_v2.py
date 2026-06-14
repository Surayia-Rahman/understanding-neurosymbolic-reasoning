# phase_01_path_quality_v2.py
# purpose: graph-aware reasoning quality scoring (v2)

import pandas as pd
from symbolic.graph_builder_v1 import TaxonomyGraphV1


class PathQualityV2:

    def __init__(self,
                 results_path="results/phase_01_taxonomy/results.csv",
                 taxonomy_path="data/raw/taxonomy_v1.csv"):

        self.df = pd.read_csv(results_path)

        builder = TaxonomyGraphV1(taxonomy_path)
        builder.load_data()
        builder.build_graph()

        self.graph = builder.get_graph()

        # precompute node importance (degree centrality proxy)
        self.node_importance = dict(self.graph.degree())

    def path_importance_score(self, row):

        # base score
        score = 0.5

        # failure handling
        if row["answer"] == "no" or row["reasoning_path"] == "":
            return 0.1

        # reward correctness
        score += 0.2

        # hop efficiency (prefer shorter paths slightly)
        if row["hops"] == 2:
            score += 0.15
        elif row["hops"] == 3:
            score += 0.1
        elif row["hops"] > 3:
            score -= 0.1

        # graph structural quality (node importance bonus)
        source = row["source"]

        importance = self.node_importance.get(source, 1)

        # normalize importance influence
        if importance >= 3:
            score += 0.1
        elif importance <= 1:
            score -= 0.05

        return max(0.0, min(1.0, score))

    def score_all(self):

        df = self.df.copy()

        df["path_quality_v2"] = df.apply(self.path_importance_score, axis=1)

        return df[[
            "source",
            "target",
            "answer",
            "hops",
            "path_quality_v2"
        ]].sort_values(by="path_quality_v2", ascending=False)

    def summary(self):

        df = self.df.copy()
        df["path_quality_v2"] = df.apply(self.path_importance_score, axis=1)

        return {
            "avg_quality": df["path_quality_v2"].mean(),
            "min_quality": df["path_quality_v2"].min(),
            "max_quality": df["path_quality_v2"].max()
        }

    def run_all(self):

        print("\n=== path quality v2 ===")
        print(self.score_all())

        print("\n=== summary ===")
        print(self.summary())


if __name__ == "__main__":
    analyzer = PathQualityV2()
    analyzer.run_all()
    
    
"""
=== path quality v2 ===
    source        target answer  hops  path_quality_v2
3    shark        animal    yes     2             0.80
4      dog        animal    yes     2             0.80
5    tulip         plant    yes     2             0.80
0      cat  living_thing    yes     3             0.75
6    snake  living_thing    yes     3             0.75
2  sparrow  living_thing    yes     3             0.75
1     rose        animal     no     0             0.10
7    eagle         plant     no     0             0.10

=== summary ===
{'avg_quality': np.float64(0.60625), 'min_quality': np.float64(0.1),'max_quality': np.float64(0.7999999999999999)}
"""
