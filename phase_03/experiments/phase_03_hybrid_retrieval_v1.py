# phase_03_hybrid_retrieval_v1.py
# purpose: hybrid embedding + graph correction system

import os
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class HybridNeuroSymbolicRetrievalV1:

    def __init__(self,
                 taxonomy_path="data/raw/taxonomy_v1.csv",
                 query_path="data/raw/neural_queries_v1.csv"):

        self.taxonomy_path = taxonomy_path
        self.query_path = query_path

        self.model = SentenceTransformer("all-MiniLM-L6-v2")

        self.graph = {}
        self.node_list = []

    def load_data(self):

        self.taxonomy_df = pd.read_csv(self.taxonomy_path).dropna()
        self.query_df = pd.read_csv(self.query_path).dropna()

    # Build graph (child → parent)
    def build_graph(self):

        self.graph = {}

        for _, row in self.taxonomy_df.iterrows():
            src = row["source"]
            tgt = row["target"]

            if src not in self.graph:
                self.graph[src] = []

            self.graph[src].append(tgt)

        self.node_list = list(set(self.taxonomy_df["source"].tolist() +
                                   self.taxonomy_df["target"].tolist()))

    # semantic retrieval (top-k)
    def get_top_k(self, query, k=3):

        node_embeddings = self.model.encode(self.node_list)
        query_embedding = self.model.encode([query])

        sims = cosine_similarity(query_embedding, node_embeddings).flatten()

        top_k_idx = np.argsort(sims)[-k:][::-1]

        return [(self.node_list[i], sims[i]) for i in top_k_idx]

    # graph validation
    def graph_distance(self, node):

        # heuristic: depth to root (living_thing)
        visited = set()
        queue = [(node, 0)]

        while queue:
            current, depth = queue.pop(0)

            if current == "living_thing":
                return depth

            visited.add(current)

            for parent in self.graph.get(current, []):
                if parent not in visited:
                    queue.append((parent, depth + 1))

        return 999

    def retrieve(self, query):

        candidates = self.get_top_k(query, k=3)

        # re-rank using graph distance
        best_node = None
        best_score = -1

        for node, sim in candidates:

            score = sim + (1.0 / (1 + self.graph_distance(node)))

            if score > best_score:
                best_score = score
                best_node = node

        return best_node, best_score


    def run(self):

        results = []

        for _, row in self.query_df.iterrows():

            query = row["query"]
            expected = row["expected_symbolic_node"]

            predicted, score = self.retrieve(query)

            results.append({
                "query": query,
                "expected": expected,
                "predicted": predicted,
                "score": score,
                "correct": predicted == expected
            })

        df = pd.DataFrame(results)

        print("\n=== HYBRID RESULTS ===")
        print(df)

        print("\n=== SUMMARY ===")
        print({
            "hybrid_accuracy": df["correct"].mean(),
            "avg_score": df["score"].mean()
        })

        output_dir = "results/phase_03_embeddings"
        os.makedirs(output_dir, exist_ok=True)

        df.to_csv(os.path.join(output_dir, "hybrid_results_v1.csv"), index=False)

        print("\nsaved hybrid results")


if __name__ == "__main__":

    model = HybridNeuroSymbolicRetrievalV1()
    model.load_data()
    model.build_graph()
    model.run()
    
"""
=== HYBRID RESULTS ===
       query expected predicted     score  correct
0     kitten      cat    animal  1.086014    False
1      puppy      dog    animal  1.184705    False
2       orca    whale     whale  0.598601     True
3     canary  sparrow      bird  0.897075    False
4       hawk    eagle      bird  0.907205    False
5   goldfish   salmon      fish  1.052759    False
6      guppy     fish    animal  1.001048    False
7  crocodile  reptile   reptile  0.917404     True
8      daisy   flower    flower  0.937707     True
9        oak    plant     plant  0.859146     True

=== SUMMARY ===
{'hybrid_accuracy': np.float64(0.4), 'avg_score': np.float32(0.9441665)}

saved hybrid results"""
