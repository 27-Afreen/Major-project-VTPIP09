# Beginner Project Walkthrough

## Project

Privacy-Preserving Deep Learning With Learnable Image Encryption on Medical Images

## Simple Explanation

Patient X has a medical scan. The hospital wants to use AI to help analyze it, but the raw scan is private. This project encrypts the scan before deep learning analysis, so the server does not directly receive the original image.

## Why This Matters

Medical images are sensitive healthcare data. A normal AI pipeline may send raw images to a server. This project changes that flow by adding image encryption before the model stage.

## Existing System

Earlier systems such as SRCNN and GDSR mainly focus on image reconstruction and super-resolution. They improve image quality, but privacy is not the main goal.

## Proposed System

The proposed system encrypts the image first, then passes the encrypted image into a deep learning workflow. This makes the project a privacy-preserving healthcare AI pipeline.

## Workflow

```text
Patient X submits symptoms
Doctor reviews the case
Lab/Admin uploads scan
Image is resized
Image is encrypted
Encrypted image is analyzed
Diagnosis result is generated
Encrypted report is stored
Doctor and Patient X view the report
```

## Technology Meanings

| Technology | Meaning |
|---|---|
| Python | Main language for backend and AI logic |
| Flask | Creates the web application |
| MySQL | Stores users, cases, and reports |
| OpenCV | Processes images |
| NumPy | Performs pixel-level calculations |
| TensorFlow/Keras | Supports deep learning models |
| CNN/DNN | Learns image patterns |
| Bootstrap | Styles the web pages |

## What You Should Be Able To Explain

1. Why raw medical image exposure is risky.
2. What learnable image encryption means.
3. How the image is transformed before model analysis.
4. How the Flask app connects patient, doctor, and lab workflows.
5. What metrics are needed to prove both model performance and privacy preservation.
