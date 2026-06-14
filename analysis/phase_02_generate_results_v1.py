# phase_02_generate_results_v1.py
# purpose: generate noisy graph reasoning results

import pandas as pd

from phase_02.symbolic.noisy_path_finder_v1 import (
    NoisyPathFinderV1
)


class Phase02ResultGeneratorV1:

    def __init__(self):

        self.finder = NoisyPathFinderV1()

    def build_query_set(self):

        return [

            ("cat", "living_thing"),
            ("rose", "animal"),
            ("sparrow", "living_thing"),
            ("shark", "animal"),
            ("dog", "animal"),
            ("tulip", "plant"),
            ("snake", "living_thing"),
            ("eagle", "plant")
        ]

    def run(self):

        records = []

        for source, target in self.build_query_set():

            result = self.finder.query(
                source,
                target
            )

            records.append({

                "source": source,
                "target": target,

                "answer": result["answer"],
                "reasoning_path": result["reasoning_path"],
                "hops": result["hops"]
            })

        df = pd.DataFrame(records)

        output_path = (
            "results/phase_02_noisy_graph/"
            "results.csv"
        )

        df.to_csv(
            output_path,
            index=False
        )

        print(
            f"\nsaved: {output_path}"
        )

        print("\n=== phase 02 results ===")
        print(df)


if __name__ == "__main__":

    generator = Phase02ResultGeneratorV1()

    generator.run()

"""saved: results/phase_02_noisy_graph/results.csv

=== phase 02 results ===
    source  ... hops
0      cat  ...    1
1     rose  ...    0
2  sparrow  ...    3
3    shark  ...    2
4      dog  ...    0
5    tulip  ...    2
6    snake  ...    3
7    eagle  ...    0

[8 rows x 5 columns]"""
