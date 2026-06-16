# Metrics Plan

This project needs two kinds of metrics:

1. Model performance metrics
2. Privacy preservation metrics

Do not add final metric values until the evaluation is actually run.

## Model Performance Metrics

| Metric | Meaning |
|---|---|
| Accuracy | How many predictions are correct overall |
| Precision | How reliable abnormal predictions are |
| Recall | How many real abnormal cases are detected |
| F1-score | Balance between precision and recall |
| Confusion matrix | Normal vs abnormal prediction breakdown |
| ROC-AUC | How well the model separates classes |

## Privacy Preservation Metrics

| Metric | Meaning |
|---|---|
| MSE | Average pixel difference between original and encrypted image |
| PSNR | Image distortion level after encryption |
| SSIM | Structural similarity between original and encrypted image |
| Entropy | Randomness in encrypted image |
| NPCR | Percentage of pixels changed by encryption |
| UACI | Average intensity change caused by encryption |

## Recommended README Table After Evaluation

| Model | Accuracy | Precision | Recall | F1-score | ROC-AUC |
|---|---:|---:|---:|---:|---:|
| DenseNet-121 | To be generated | To be generated | To be generated | To be generated | To be generated |
| XceptionNet | To be generated | To be generated | To be generated | To be generated | To be generated |
| Majority Vote | To be generated | To be generated | To be generated | To be generated | To be generated |

| Encryption Method | MSE | PSNR | SSIM | Entropy | NPCR | UACI |
|---|---:|---:|---:|---:|---:|---:|
| Negative-positive + channel shuffle + smoothing | To be generated | To be generated | To be generated | To be generated | To be generated | To be generated |
