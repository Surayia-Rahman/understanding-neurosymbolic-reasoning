# roadmap

## phase 01
biological taxonomy graph

## phase 02
multi-hop reasoning

## phase 03
contradictions and exceptions

## phase 04
scientific knowledge graphs

## phase 05
llm integration

## phase 06
neurosymbolic evaluation

## phase 07
advanced analytics and explainability

## phase 01 summary

we built a symbolic reasoning system based on a taxonomy graph.

we now track:

- reasoning outputs (results.csv)
- experiment metrics (metrics_summary.csv)
- graph structure metrics (graph_metrics.csv)
- node importance (graph_centrality.csv)
- graph visualization artifacts (figures/)
- failure diagnostics (failure analysis + heatmaps)

this system allows us to:
- evaluate reasoning correctness
- measure graph connectivity effects
- identify structural weaknesses in knowledge representation
- generate reproducible experimental logs


## phase 02 - graph robustness experiments

objective:
evaluate symbolic reasoning performance under controlled graph perturbations.

components:
- noisy graph generation
- noisy path execution
- robustness evaluation
- failure propagation analysis
- explainability degradation analysis

phase 02 milestone--

implemented physical graph perturbation
through controlled edge removal and
edge corruption.

this enables direct comparison between
clean and noisy symbolic reasoning
environments.

phase 02 progress--

completed:
- noisy graph generation
- noisy graph execution
- path deviation analysis
- hallucination-like shortcut detection

next:
- multi-seed robustness experiments
- statistical robustness analysis
- faithfulness metrics

-----------------

# phase roadmap

## phase 01 — symbolic reasoning baseline

status: complete

completed:
- taxonomy graph construction
- path-based reasoning
- graph analytics
- explainability metrics
- failure analysis

artifacts:
- graph metrics
- node vulnerability analysis
- graph visualizations

---

## phase 02 — robustness under graph corruption

status: complete

completed:
- noisy graph generation
- graph perturbation experiments
- noisy reasoning execution
- path deviation analysis
- hallucination-like shortcut detection
- multi-seed robustness experiments
- robustness visualization
- robustness reporting

key findings:
- reasoning paths changed in 50% of evaluated cases
- successful reasoning can become failure under corruption
- shortcut explanations can emerge under noisy conditions
- three reasoning regimes observed:
  - stable
  - degraded
  - collapsed

artifacts:
- robustness_experiments.csv
- robustness_report.md
- success_rate_by_seed.png
- hop_distribution.png

---

## phase 03 — neural similarity layer

status: planned

goals:
- semantic retrieval
- embedding generation
- symbolic vs neural comparison
- neurosymbolic fusion

