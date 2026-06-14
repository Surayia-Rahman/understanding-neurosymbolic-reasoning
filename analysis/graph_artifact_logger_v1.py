# graph_artifact_logger_v1.py
# purpose: save graph analysis artifacts

import os
import pandas as pd
from datetime import datetime


class GraphArtifactLoggerV1:

    def __init__(
        self,
        results_dir="results/phase_01_taxonomy"
    ):
        self.results_dir = results_dir

        os.makedirs(
            os.path.join(results_dir, "figures"),
            exist_ok=True
        )

    def save_graph_metrics(
        self,
        metrics
    ):
        filepath = os.path.join(
            self.results_dir,
            "graph_metrics.csv"
        )

        row = {
            "timestamp": datetime.now().isoformat(),
            **metrics
        }

        df_new = pd.DataFrame([row])

        if os.path.exists(filepath):
            df_existing = pd.read_csv(filepath)
            df_final = pd.concat(
                [df_existing, df_new],
                ignore_index=True
            )
        else:
            df_final = df_new

        df_final.to_csv(
            filepath,
            index=False
        )

    def save_centrality(
        self,
        centrality_data
    ):
        filepath = os.path.join(
            self.results_dir,
            "graph_centrality.csv"
        )

        rows = []

        timestamp = datetime.now().isoformat()

        for node, degree in centrality_data:
            rows.append({
                "timestamp": timestamp,
                "node": node,
                "degree": degree
            })

        df_new = pd.DataFrame(rows)

        if os.path.exists(filepath):
            df_existing = pd.read_csv(filepath)
            df_final = pd.concat(
                [df_existing, df_new],
                ignore_index=True
            )
        else:
            df_final = df_new

        df_final.to_csv(
            filepath,
            index=False
        )