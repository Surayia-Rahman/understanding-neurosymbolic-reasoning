# phase 02 path deviation findings

experiment:
compare reasoning behavior between clean and noisy graphs.

results:

- 50 percent of reasoning paths changed.
- 12.5 percent of successful queries became failures.
- one hallucination-like shortcut was detected.
- average path length decreased by 0.5 hops.

key observation:

graph corruption does not primarily destroy reasoning.

instead, it frequently changes the reasoning pathway while preserving the final answer.

implication:

correctness and reasoning faithfulness should be evaluated separately.