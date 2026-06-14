# phase_02_multi_seed_robustness_v1.py
# purpose: run noisy graph experiments across multiple seeds
# and measure robustness stability

import pandas as pd

from phase_02.symbolic.noisy_graph_builder_v1 import NoisyGraphBuilderV1
from phase_02.symbolic.noisy_path_finder_v1 import NoisyPathFinderV1


class MultiSeedRobustnessV1:

    def __init__(self, seeds=range(1, 21)):

        self.seeds = seeds

        self.query_set = [
            ("cat", "living_thing"),
            ("rose", "animal"),
            ("sparrow", "living_thing"),
            ("shark", "animal"),
            ("dog", "animal"),
            ("tulip", "plant"),
            ("snake", "living_thing"),
            ("eagle", "plant")
        ]

    def run_single_seed(self, seed):

        builder = NoisyGraphBuilderV1()

        noisy_graph = builder.create_noisy_graph(seed=seed)

        finder = NoisyPathFinderV1()
        finder.graph = noisy_graph  # inject controlled graph

        results = []

        for source, target in self.query_set:

            res = finder.query(source, target)

            results.append({
                "seed": seed,
                "source": source,
                "target": target,
                "answer": res["answer"],
                "hops": res["hops"],
                "reasoning_path": res["reasoning_path"]
            })

        return results

    def run(self):

        all_results = []

        for seed in self.seeds:

            print(f"\nrunning seed {seed}...")

            seed_results = self.run_single_seed(seed)

            all_results.extend(seed_results)

        df = pd.DataFrame(all_results)

        output_path = "results/phase_02_noisy_graph/robustness_experiments.csv"

        df.to_csv(output_path, index=False)

        print("\n=== saved robustness results ===")
        print(output_path)

        return df

    def summary(self, df):

        grouped = df.groupby("seed")

        summary = grouped.agg({
            "hops": "mean",
            "answer": lambda x: (x == "yes").mean()
        }).rename(columns={
            "hops": "avg_hops",
            "answer": "success_rate"
        })

        return summary


if __name__ == "__main__":

    runner = MultiSeedRobustnessV1(seeds=range(1, 11))

    df = runner.run()

    print("\n=== summary by seed ===")
    print(runner.summary(df))
    
"""
running seed 1...

running seed 2...

running seed 3...

running seed 4...

running seed 5...

running seed 6...

running seed 7...

running seed 8...

running seed 9...

running seed 10...

=== saved robustness results ===
results/phase_02_noisy_graph/robustness_experiments.csv

=== summary by seed ===
      avg_hops  success_rate
seed                        
1        1.125         0.500
2        1.625         0.625
3        1.500         0.625
4        0.625         0.375
5        1.250         0.500
6        0.750         0.375
7        0.875         0.375
8        0.500         0.250
9        0.000         0.000
10       1.625         0.750"""
