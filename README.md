# 🧠 Neuro-Symbolic Reasoning: Graphs, Embeddings & Hybrid AI Systems

![Python](https://img.shields.io/badge/python-3.10+-blue)
![Status](https://img.shields.io/badge/status-research--prototype-orange)
![Scope](https://img.shields.io/badge/scope-neuro--symbolic--AI-purple)

---

## 📌 Project Overview

This project investigates **neuro-symbolic reasoning systems** across three paradigms:

1. Symbolic reasoning via taxonomy graphs  
2. Robustness under structural noise  
3. Neural embeddings + hybrid fusion models  

The objective is to evaluate how **semantic similarity and symbolic structure interact under controlled perturbations and retrieval tasks**.

In professional words,

> Can neural embeddings and symbolic graph reasoning be combined without losing structural correctness or semantic generalization?

---

## 🧱 System architecture


<img width="1536" height="1024" alt="0e8eb087-1330-4332-bc71-5535e2252a26" src="https://github.com/user-attachments/assets/752317c7-25ef-41c9-93a0-805dfd4222c0" />


---

## 📁 Repository 

## Core Logic

| Folder | Purpose |
|--------|--------|
| `symbolic/` | Graph construction + path reasoning engine |
| `analysis/` | All experimental pipelines (Phase 01 & 02) |
| `phase_03/embeddings/` | Neural embedding models |
| `phase_03/experiments/` | Hybrid + evaluation experiments |

---

## Data Layer

| Folder | Purpose |
|--------|--------|
| `data/raw/` | Original taxonomy + query datasets |
| `data/processed/` | Cleaned experimental datasets |
| `data/generated/` | (Optional) synthetic or derived datasets |

---

## Results 

All outputs are stored in:

```
results/
```

### Phase-wise outputs:

| Phase | Outputs |
|------|--------|
| Phase 01 | graph metrics, centrality, vulnerability |
| Phase 02 | robustness experiments, noise analysis |
| Phase 03 | embeddings, hybrid retrieval, similarity scores |

---

## 📊 KEY VISUAL RESULTS

### Phase 01 — Graph Structure

- Node vulnerability analysis
- Centrality distributions
- Multi-hop reasoning paths

📌 Example outputs:
- `graph_visualization_v1.png`
- `node_vulnerability_v1.png`

---

### Phase 02 — Robustness Under Noise

- Multi-seed graph corruption tests
- Success/failure degradation curves
- Regime classification (stable / degraded / collapsed)

📌 Key figures:
- `success_rate_by_seed.png`
- `hop_distribution.png`

---

### Phase 03 — Embeddings & Hybrid Model

- Semantic similarity distributions
- TF-IDF vs embedding comparison
- Hybrid retrieval scoring

📌 Key figures:
- `similarity_distribution_v1.png`

---

## 📊 Experiment results

### Model Performance Comparison

| Model | Accuracy | Avg Similarity | Key Strength | Key Weakness |
|------|----------|----------------|--------------|---------------|
| TF-IDF | 0.10 | 0.00 | Fast lexical match | No semantics |
| Embeddings | 0.50 | 0.60 | Semantic generalization | Weak structure |
| Hybrid | 0.40 | 0.94 | Balanced fusion | Hub bias |

---

### Robustness Summary (Phase 02)

| Metric | Value |
|------|------|
| Stable seeds | 3 / 10 |
| Degraded seeds | 5 / 10 |
| Collapsed seeds | 2 / 10 |
| Avg success drop | ~5% |

---

## ⚠️ Key findings

### 1. Symbolic systems
✔ Precise reasoning paths  
❌ Extremely fragile under noise  

---

### 2. Neural embeddings
✔ Strong semantic generalization  
❌ Ignore hierarchical constraints  

---

### 3. Hybrid systems
✔ Improved overall recall  
❌ Introduce structural bias (“hub dominance”)  

---

## 🧠 Fundamental Insight

> Semantic similarity and symbolic correctness are not naturally aligned and require explicit structural constraints or learned alignment mechanisms.

---

## 🧠 Failure reasoning

| Type | Description |
|------|-------------|
| Lexical failure | TF-IDF mismatch |
| Semantic drift | embedding confusion |
| Structural collapse | broken graph path |
| Hub bias | hybrid over-reliance on central nodes |

---

## 🚀 To run,

### Install dependencies
```bash
pip install -r requirements.txt
```

---

### Phase 01
```bash
python -m analysis.phase_01_graph_analysis
```

---

### Phase 02
```bash
python -m analysis.phase_02_robustness_report_v1
```

---

### Phase 03 (Semantic)
```bash
python -m phase_03.embeddings.semantic_embedding_generator_v1
```

---

### Phase 03 (Hybrid)
```bash
python -m phase_03.experiments.phase_03_hybrid_retrieval_v1
```

---

## 📌 Outputs

All generated collectibles

```
results/
```

Includes:
- CSV metrics
- robustness logs
- similarity scores
- plots and figures

---

## Tests

Minimal validation suite:

```
tests/
```

Ensures:
- graph integrity
- query consistency

---

## Future work

- Learnable graph–embedding alignment
- Ontology-aware transformer models
- Adaptive hybrid weighting
- Constraint-based reasoning architectures

---

# 👤 AUTHOR NOTE

This is a research prototype exploring neuro-symbolic reasoning under structural perturbation, semantic drift, and hybrid fusion collapse modes.

