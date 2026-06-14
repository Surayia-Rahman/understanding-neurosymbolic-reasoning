# phase_01_path_decomposition_v1.py
# purpose: break reasoning paths into hop-level explainability signals

import pandas as pd


class PathDecompositionV1:

    def __init__(self,
                 path="results/phase_01_taxonomy/results.csv"):

        self.df = pd.read_csv(path)

    def split_path(self, path_str):
        """
        converts 'a -> b -> c' into list of edges
        """
        nodes = [x.strip() for x in path_str.split("->")]
        edges = []

        for i in range(len(nodes) - 1):
            edges.append((nodes[i], nodes[i + 1]))

        return edges

    def hop_score(self, row):
        """
        assigns contribution score per hop
        """

        if pd.isna(row["reasoning_path"]) or row["reasoning_path"] == "":
            return []

        edges = self.split_path(row["reasoning_path"])

        hop_scores = []

        base = 1.0 if row["answer"] == "yes" else 0.2

        for i, (src, dst) in enumerate(edges):

            # deeper hops slightly discounted
            depth_penalty = 0.05 * i

            score = base - depth_penalty

            hop_scores.append({
                "source": row["source"],
                "from": src,
                "to": dst,
                "hop_index": i,
                "hop_score": round(max(0.0, score), 3)
            })

        return hop_scores

    def expand_all(self):

        all_rows = []

        for _, row in self.df.iterrows():

            hops = self.hop_score(row)
            all_rows.extend(hops)

        return pd.DataFrame(all_rows)

    def summary(self):

        df = self.expand_all() 

        return {
            "avg_hop_score": df["hop_score"].mean(),
            "min_hop_score": df["hop_score"].min(),
            "max_hop_score": df["hop_score"].max(),
            "total_hops": len(df)
        }

    def run_all(self):

        df = self.expand_all()

        print("\n=== hop-level explanation table ===")
        print(df)

        print("\n=== summary ===")
        print(self.summary())


if __name__ == "__main__":
    analyzer = PathDecompositionV1()
    analyzer.run_all()
    
"""
=== hop-level explanation table ===
     source     from            to  hop_index  hop_score
0       cat      cat        mammal          0       1.00
1       cat   mammal        animal          1       0.95
2       cat   animal  living_thing          2       0.90
3   sparrow  sparrow          bird          0       1.00
4   sparrow     bird        animal          1       0.95
5   sparrow   animal  living_thing          2       0.90
6     shark    shark          fish          0       1.00
7     shark     fish        animal          1       0.95
8       dog      dog        mammal          0       1.00
9       dog   mammal        animal          1       0.95
10    tulip    tulip        flower          0       1.00
11    tulip   flower         plant          1       0.95
12    snake    snake       reptile          0       1.00
13    snake  reptile        animal          1       0.95
14    snake   animal  living_thing          2       0.90

=== summary ===
{'avg_hop_score': np.float64(0.9599999999999997), 'min_hop_score': np.float64(0.9), 'max_hop_score': np.float64(1.0), 'total_hops': 15}
"""
