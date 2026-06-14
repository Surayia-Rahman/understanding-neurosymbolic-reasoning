import pandas as pd

def test_no_missing_nodes():
    df = pd.read_csv("data/raw/taxonomy_v1.csv")
    assert df["source"].notnull().all()
    assert df["target"].notnull().all()