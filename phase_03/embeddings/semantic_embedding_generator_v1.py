# semantic_embedding_generator_v1.py
# purpose: semantic neural retrieval baseline using sentence-transformers

import os
import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


class SemanticNeuralRetrievalV1:

    def __init__(self,
                 taxonomy_path="data/raw/taxonomy_v1.csv",
                 query_path="data/raw/neural_queries_v1.csv"):

        self.taxonomy_path = taxonomy_path
        self.query_path = query_path

        self.taxonomy_df = None
        self.query_df = None

        self.node_list = None

        # lightweight semantic model
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def load_data(self):

        self.taxonomy_df = pd.read_csv(self.taxonomy_path).dropna()
        self.query_df = pd.read_csv(self.query_path).dropna()


    def extract_nodes(self):

        sources = self.taxonomy_df["source"].tolist()
        targets = self.taxonomy_df["target"].tolist()

        return list(set(sources + targets))


    def build_embeddings(self):

        self.node_list = self.extract_nodes()

        self.node_embeddings = self.model.encode(
            self.node_list,
            convert_to_numpy=True,
            show_progress_bar=False
        )

    # retrieve best node
    def retrieve(self, query):

        query_embedding = self.model.encode([query], convert_to_numpy=True)

        similarities = cosine_similarity(
            query_embedding,
            self.node_embeddings
        ).flatten()

        best_idx = int(np.argmax(similarities))

        return (
            self.node_list[best_idx],
            float(similarities[best_idx])
        )

   
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
                "similarity": score,
                "correct": predicted == expected
            })

        df = pd.DataFrame(results)

        accuracy = df["correct"].mean()

        print("\n=== SEMANTIC RETRIEVAL RESULTS ===")
        print(df)

        print("\n=== SUMMARY ===")
        print({
            "semantic_accuracy": accuracy,
            "avg_similarity": df["similarity"].mean()
        })

        output_dir = "results/phase_03_embeddings"
        os.makedirs(output_dir, exist_ok=True)

        output_path = os.path.join(output_dir, "semantic_retrieval_v1.csv")
        df.to_csv(output_path, index=False)

        print(f"\nsaved: {output_path}")

        return df


if __name__ == "__main__":

    model = SemanticNeuralRetrievalV1()
    model.load_data()
    model.build_embeddings()
    model.run()
    
"""
=== SEMANTIC RETRIEVAL RESULTS ===
       query expected  ... similarity  correct
0     kitten      cat  ...   0.788211     True
1      puppy      dog  ...   0.804007     True
2       orca    whale  ...   0.348601     True
3     canary  sparrow  ...   0.563741    False
4       hawk    eagle  ...   0.573872    False
5   goldfish   salmon  ...   0.719426    False
6      guppy     fish  ...   0.562113     True
7  crocodile  reptile  ...   0.613655    False
8      daisy   flower  ...   0.604374     True
9        oak    plant  ...   0.482614    False

[10 rows x 5 columns]

=== SUMMARY ===
{'semantic_accuracy': np.float64(0.5), 'avg_similarity': np.float64(0.606061327457428)}

saved: results/phase_03_embeddings\semantic_retrieval_v1.csv
"""
