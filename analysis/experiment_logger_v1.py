# experiment_logger_v1.py
# purpose: persist reasoning experiments as structured datasets

import os
import pandas as pd
from datetime import datetime


class ExperimentLoggerV1:
    def __init__(self, save_path="results/phase_01_taxonomy/results.csv"):
        self.save_path = save_path

        # ensure directory exists
        os.makedirs(os.path.dirname(self.save_path), exist_ok=True)

        # create file if it doesn't exist
        if not os.path.exists(self.save_path):
            df = pd.DataFrame(columns=[
                "timestamp",
                "source",
                "target",
                "answer",
                "reasoning_path",
                "hops",
                "experiment_id"
            ])
            df.to_csv(self.save_path, index=False)

    def log_batch(self, results, experiment_id="phase_01_batch_01"):
        """
        results: list of dicts from reasoning engine
        """

        timestamp = datetime.now().isoformat()

        rows = []

        for r in results:
            rows.append({
                "timestamp": timestamp,
                "source": r["source"],
                "target": r["target"],
                "answer": r["answer"],
                "reasoning_path": r["reasoning_path"],
                "hops": r["hops"],
                "experiment_id": experiment_id
            })

        df_new = pd.DataFrame(rows)

        # append safely
        df_existing = pd.read_csv(self.save_path)
        df_final = pd.concat([df_existing, df_new], ignore_index=True)

        df_final.to_csv(self.save_path, index=False)

        return df_final