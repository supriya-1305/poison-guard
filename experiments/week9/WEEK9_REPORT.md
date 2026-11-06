# Week 9 – Poisoning Rate Experiment Analysis

## Objective
Evaluate the effect of different backdoor poisoning rates on ResNet18 using CIFAR-10.

## Experimental Configuration
- Dataset: CIFAR-10
- Model: ResNet18
- Trigger: 4x4 white square, bottom-right
- Target class: 0 (airplane)
- Epochs: 2 per experiment (accelerated run)
- Device: Apple Silicon MPS

## Results
| Poisoning Rate | Clean Accuracy | Attack Success Rate |
|---:|---:|---:|
| 0% | 75.04% | 1.43% |
| 1% | 75.16% | 92.32% |
| 3% | 72.57% | 93.22% |
| 5% | 73.75% | 95.24% |
| 10% | 73.49% | 97.44% |

## Graphs
- graphs/clean_accuracy_comparison.png
- graphs/attack_success_comparison.png
- graphs/week9_combined_comparison.png

## Analysis
The experiments show a substantial increase in attack success rate as poisoning increases. Clean accuracy remains comparatively similar. This demonstrates that clean accuracy alone is insufficient to assess backdoor security.

## Limitation
Each experiment used 2 training epochs for accelerated execution. Results should not be presented as equivalent to a full 10-epoch evaluation.

## Conclusion
Backdoor poisoning can produce high attack success while maintaining reasonable clean accuracy. Evaluation should therefore include both clean accuracy and attack success rate.
