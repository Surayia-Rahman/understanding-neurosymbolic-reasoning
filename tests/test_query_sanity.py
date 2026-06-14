import pandas as pd

def test_queries_valid():
    df = pd.read_csv("data/raw/neural_queries_v1.csv")
    assert df["query"].notnull().all()
    assert df["expected_symbolic_node"].notnull().all()