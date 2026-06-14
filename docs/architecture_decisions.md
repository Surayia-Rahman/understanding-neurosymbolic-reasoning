# architecture decisions

## decision 001

title:
use csv for knowledge graph storage

reason:
- easy to inspect
- pandas friendly
- supports future analytics
- simple version control

status:
accepted

---

## decision 002

title:
preserve all project phases

reason:
- reproducibility
- experiment tracking
- portfolio transparency

status:
accepted

## decision 004

title:
introduce node-level failure diagnostics

reason:
system-level metrics were insufficient to understand why failures occur

solution:
compute node-level failure and success scores to identify weak regions in the graph

impact:
enables structural debugging of knowledge representation