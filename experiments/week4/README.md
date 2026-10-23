# PoisonGuard Week 4 — Backdoor Trigger Visualization

## Objective

Visualize a controlled backdoor trigger applied to a CIFAR-10 image.

## Input

- `data/backdoor/images.npy`
- `data/backdoor/metadata.json`

## Visualization

A clean image and a backdoored image were displayed side by side to
provide visual evidence of the controlled trigger.

## Output

`experiments/week4/figures/backdoor_trigger_example.png`

## Verification

- Backdoor metadata contains clean and backdoored samples.
- The generated PNG is valid.
- Clean and backdoored image arrays are not identical.

## Purpose

The visualization provides evidence for the controlled backdoor
simulation used in the Week 4 PoisonGuard experiment.
