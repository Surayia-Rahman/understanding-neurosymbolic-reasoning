# Hybrid Neuro-Symbolic Analysis

## Observation
Combining embeddings with graph bias improves structure awareness but introduces hub dominance.

## Result
- Accuracy: 0.4

## Failure Mode
Graph bias overpowers semantic signal causing over-generalization (e.g., mapping to 'animal').

## Conclusion
Naive fusion is unstable without learned weighting or constraint optimization.