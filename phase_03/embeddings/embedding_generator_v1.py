# embedding_generator_v1.py
# purpose: TF-IDF based neural-to-symbolic retrieval baseline (Phase 03 v1)

import os
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class TFIDFNeuralRetrievalV1:

    def __init__(self,
                 taxonomy_path="data/raw/taxonomy_v1.csv",
                 query_path="data/raw/neural_queries_v1.csv"):

        self.taxonomy_path = taxonomy_path
        self.query_path = query_path

        self.taxonomy_df = None
        self.query_df = None

        self.node_list = None
        self.vectorizer = TfidfVectorizer()

    def load_data(self):

        self.taxonomy_df = pd.read_csv(self.taxonomy_path)
        self.query_df = pd.read_csv(self.query_path)

        self.taxonomy_df = self.taxonomy_df.dropna()
        self.query_df = self.query_df.dropna()

    # Extract graph nodes
    def extract_nodes(self):

        sources = self.taxonomy_df["source"].tolist()
        targets = self.taxonomy_df["target"].tolist()

        nodes = list(set(sources + targets))

        return nodes


    # Build TF-IDF embeddings
    def build_embeddings(self):

        self.node_list = self.extract_nodes()

        self.tfidf_matrix = self.vectorizer.fit_transform(self.node_list)

    # Retrieve best match
    def retrieve(self, query):

        query_vec = self.vectorizer.transform([query])

        similarities = cosine_similarity(
            query_vec,
            self.tfidf_matrix
        ).flatten()

        best_idx = similarities.argmax()

        best_node = self.node_list[best_idx]
        best_score = similarities[best_idx]

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
                "similarity": score,
                "correct": predicted == expected
            })

        df = pd.DataFrame(results)

        accuracy = df["correct"].mean()

        print("\n=== RETRIEVAL RESULTS ===")
        print(df)

        print("\n=== SUMMARY ===")
        print({
            "retrieval_accuracy": accuracy,
            "avg_similarity": df["similarity"].mean()
        })

        output_dir = "results/phase_03_embeddings"
        os.makedirs(output_dir, exist_ok=True)

        output_path = os.path.join(output_dir, "retrieval_results_v1.csv")
        df.to_csv(output_path, index=False)

        print(f"\nsaved: {output_path}")

        return df

if __name__ == "__main__":

    model = TFIDFNeuralRetrievalV1()
    model.load_data()
    model.build_embeddings()
    model.run()
    
"""
PS C:\Users\Surayia Rahman\Downloads\neurosymbolic-reasoning> python -m phase_03.embeddings.embedding_generator_v1

=== RETRIEVAL RESULTS ===
       query expected  ... similarity  correct
0     kitten      cat  ...        0.0    False
1      puppy      dog  ...        0.0    False
2       orca    whale  ...        0.0     True
3     canary  sparrow  ...        0.0    False
4       hawk    eagle  ...        0.0    False
5   goldfish   salmon  ...        0.0    False
6      guppy     fish  ...        0.0    False
7  crocodile  reptile  ...        0.0    False
8      daisy   flower  ...        0.0    False
9        oak    plant  ...        0.0    False

[10 rows x 5 columns]

=== SUMMARY ===
{'retrieval_accuracy': np.float64(0.1), 'avg_similarity': np.float64(0.0)}

saved: results/phase_03_embeddings\retrieval_results_v1.csv"""
