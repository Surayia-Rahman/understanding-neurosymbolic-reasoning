# graph_builder_v1.py
# purpose: load taxonomy_v1.csv and build a directed graph using networkx

import pandas as pd
import networkx as nx


class TaxonomyGraphV1:
    def __init__(self, csv_path):
        self.csv_path = csv_path
        self.graph = nx.DiGraph()

    def load_data(self):
        # load csv into pandas dataframe
        self.df = pd.read_csv(self.csv_path)

    def build_graph(self):
        # add edges: source -> target
        for _, row in self.df.iterrows():
            source = row["source"]
            target = row["target"]
            relation = row["relation"]

            # we include relation as edge attribute for future expansion
            self.graph.add_edge(source, target, relation=relation)

    def get_graph(self):
        return self.graph


if __name__ == "__main__":
    # test run (manual check)
    csv_path = "data/raw/taxonomy_v1.csv"

    tg = TaxonomyGraphV1(csv_path)
    tg.load_data()
    tg.build_graph()

    print("nodes:", tg.graph.nodes())
    print("edges:", tg.graph.edges(data=True))