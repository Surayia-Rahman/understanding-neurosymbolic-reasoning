# Phase 02 Robustness Report

## Seed-level summary

      avg_hops  success_rate     regime
seed                                   
1        1.125         0.500   degraded
2        1.625         0.625     stable
3        1.500         0.625     stable
4        0.625         0.375   degraded
5        1.250         0.500   degraded
6        0.750         0.375   degraded
7        0.875         0.375   degraded
8        0.500         0.250  collapsed
9        0.000         0.000  collapsed
10       1.625         0.750     stable


## Regime distribution

regime
degraded     5
stable       3
collapsed    2
Name: count, dtype: int64


## Key findings

- reasoning stability varies significantly across graph perturbations
- some seeds collapse completely (0% success rate)
- hop distributions shift toward shorter paths under noise