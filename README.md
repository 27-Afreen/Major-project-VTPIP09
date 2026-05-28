# Privacy-Preserving Deep Learning With Learnable Image Encryption on Medical Images

**VTPIP09 Major Project** - A secure end-to-end medical imaging platform that encrypts patient scan images on the client side using an enhanced SKK learnable encryption scheme before sending them to a cloud server for DNN-based diagnosis, ensuring patient data privacy without compromising model performance.

---

## Screenshots

### Home Page
![Home Page](Screenshots/home_page.png)

### Login Dashboard
![Login Dashboard](Screenshots/login_dashboard.png)

### Doctor Registration
![Doctor Registration](Screenshots/doctor_registration.png)

### Doctor Dashboard
![Doctor Dashboard](Screenshots/doctor_dashboard.png)

### Patient Dashboard
![Patient Dashboard](Screenshots/Patient_dashboard.png)

### Patient Reports
![Patient Reports](Screenshots/Pt_Reports.png)

---

## Abstract

The growing dependency on cloud servers for training Deep Neural Network (DNN) models raises serious privacy concerns, especially in the medical domain. Cloud servers are considered **semi-honest**  they process data correctly but may attempt to observe and exploit it. Sharing raw medical images with such servers exposes sensitive patient data.

This project proposes an enhanced **Learnable Image Encryption Scheme** based on the original SKK scheme. Medical images are encrypted on the client side before being transmitted to the server. The encrypted images are then used for DNN training using **DenseNet-121** and **XceptionNet** models. The experiment demonstrates that privacy can be effectively preserved while maintaining diagnostic accuracy comparable to training on raw images.

---

## Problem Statement - Existing System

The existing approach (SRCNN/GDSR-based) has the following limitations:

- **No Privacy Protection:** Raw medical images are sent directly to cloud servers for DNN training, exposing sensitive patient information
- **Vulnerable Encryption:** Previous encryption schemes (early SKK variants) have been partially attacked in prior studies
- **SRCNN Limitation:** Uses bicubic interpolation for super-resolution without external knowledge — lacks privacy awareness
- **GDSR Network:** Left-right asymmetric SR architecture improves quality but does not address data privacy

---

## Proposed Solution

Our system introduces an enhanced version of the SKK encryption scheme with three stages:

### Stage 1 - Negative-Positive Transformation
Inverts all pixel values (`new_pixel = 255 - pixel`) to obscure the visual content of the image before it leaves the client.

### Stage 2 - Color Channel Shuffling
Randomly shuffles the RGB channels of the image using a secret permutation key, making colour-based pattern recognition impossible without the key.

### Stage 3 - Statistical Smoothing (4 Filters)
Divides the image into fixed-size blocks and applies one of the following filters to fill all elements of a block with a single statistical value:

| Filter | Operation |
|--------|-----------|
| Median Filter | Fills block with median pixel value |
| Mean Filter | Fills block with mean pixel value |
| Maximum Filter | Fills block with maximum pixel value |
| Minimum Filter | Fills block with minimum pixel value |

After all three stages, the encrypted image is sent to the server for DNN training.

---

## DNN Models Used

| Model | Architecture | Input Size | Batch Size | Optimizer |
|-------|-------------|-----------|-----------|-----------|
| DenseNet-121 | Dense Connections CNN | 256 × 256 | 35 | SGD (momentum=0.9) |
| XceptionNet | Depthwise Separable CNN | 256 × 256 | 35 | SGD (momentum=0.9) |

Both models are trained on encrypted medical images from open-source datasets. The final diagnosis is determined by a majority vote between both models.

---

## System Workflow

```
Patient submits symptoms via web portal
              ↓
Doctor reviews and forwards case to Lab
              ↓
Lab uploads medical scan image
              ↓
[CLIENT SIDE]
Image encrypted using Enhanced SKK Scheme:
  → Negative-Positive Transformation
  → Color Channel Shuffling
  → Statistical Smoothing (Median Filter)
              ↓
Encrypted image sent to server (cloud)
              ↓
[SERVER SIDE]
Data augmentation on encrypted image
              ↓
DenseNet-121 & XceptionNet run diagnosis
              ↓
Secure 10-character access token generated
              ↓
Doctor views encrypted scan + diagnosis result
Patient views scan using personal access key
```

---

## System Architecture

The system follows a three-tier architecture:

- **Client Tier:** Patient, Doctor, Admin web portal (Flask + Bootstrap)
- **Application Tier:** Encryption module (SKK), DNN models (DenseNet-121, XceptionNet), Flask backend
- **Data Tier:** MySQL database storing users, doctor records, symptom submissions, encrypted reports

---

## What Has Been Achieved

| Feature | Details | Status |
|---------|---------|--------|
| Role-based web portal | Admin, Doctor, Patient dashboards | 
| Patient registration & login | Email + password authentication | 
| Doctor registration & login | Email + password + department | 
| Symptom submission workflow | Patient → Doctor → Lab → Report | 
| Scan image upload by lab | File upload with secure storage | 
| SKK Encryption — Stage 1 | Negative-positive transformation | 
| SKK Encryption — Stage 2 | Color channel shuffling | 
| SKK Encryption — Stage 3 | Median / Mean / Max / Min filters | 
| Image resized to 256×256 | Before DNN input as per requirement |
| DenseNet-121 integration | Pre-trained model for medical diagnosis | 
| XceptionNet integration | Pre-trained model for cross-validation |  
| Majority-vote final diagnosis | Combined result from both models | 
| Encrypted image displayed to doctor | Doctor views encrypted scan | 
| AI diagnosis result shown | Normal / Abnormal with confidence % | 
| Secure access token (10-char) | Patient uses key to access report | 
| MySQL database (4 tables) | user, doctor, userdet, sreport | 
| Privacy details shown in UI | Encryption scheme details visible | 

---

## Project Outcome

The implemented system demonstrates:

1. **Privacy Preservation:** Medical images are never transmitted in raw form. The enhanced SKK scheme with statistical smoothing ensures the encrypted image visually reveals no diagnostic information to a semi-honest server.

2. **DNN Compatibility:** Both DenseNet-121 and XceptionNet successfully process the encrypted 256×256 images and produce diagnosis results, proving that privacy-preserving DNN training is feasible.

3. **Trade-off Achievement:** The system balances the trade-off between model accuracy and image security — the DNN models retain diagnostic capability even on encrypted inputs.

4. **Improved Security Over Existing SKK:** The addition of statistical smoothing (median, mean, max, min filters) hardens the encryption against partial attacks that affected earlier SKK variants.

5. **End-to-End Secure Workflow:** From symptom submission to encrypted scan report delivery, the entire pipeline is secured with role-based access and cryptographic tokens.

---

## What More Can Be Done

| Enhancement | Details |
|-------------|---------|
| Train DenseNet-121 from scratch | Fine-tune on labelled chest X-ray / MRI datasets |
| Train XceptionNet from scratch | Domain-specific training for higher accuracy |
| Accuracy comparison study | Raw vs encrypted image training accuracy metrics |
| Privacy attack simulation | Test resistance to pixel inference and channel attacks |
| Block size optimisation | Evaluate best block size (3×3, 8×8, 16×16) for each filter |
| All 4 filter comparison | Show accuracy difference between median/mean/max/min |
| Confusion matrix & metrics | Precision, recall, F1-score on diagnosis results |
| PSNR / SSIM analysis | Measure visual distortion introduced by encryption |
| Real medical dataset training | CheXNet, NIH Chest X-ray, ISIC skin dataset |
| Client-side JavaScript encryption | Encrypt in browser before upload using WebCrypto API |

---

## Tech Stack

| Technology | Purpose |
|-----------|---------|
| Python 3 | Backend language |
| Flask | Web framework |
| MySQL | Database |
| OpenCV | Image processing & encryption |
| NumPy | Statistical filter operations |
| TensorFlow / Keras | DenseNet-121 & XceptionNet |
| Bootstrap 4 | Frontend UI |
| HTML / Jinja2 | Templating |

---

## Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/27-Afreen/Major-project-VTPIP09.git
cd Major-project-VTPIP09
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
pip install tensorflow
```

### 3. Start MySQL and Setup Database
```bash
net start MySQL
```
Open MySQL Command Line Client:
```sql
SOURCE path/to/vtpip09_2022_setup.sql;
SOURCE path/to/update_db.sql;
```

### 4. Configure app.py
```python
conn = mysql.connector.connect(
    host="localhost",
    port=3307,
    user="root",
    password="your_password",
    database="vtpip09_2022"
)
```

### 5. Run
```bash
python app.py
```
Open: **http://127.0.0.1:5000**

---

## Database Schema

| Table | Columns |
|-------|---------|
| `user` | name, email, password, mobile, location |
| `doctor` | name, email, password, mobile, department |
| `userdet` | id, name, email, symptoms, DocId, status |
| `sreport` | id, name, uid, did, filename, key1, diagnosis, densenet_conf, xception_conf |

---

## Advantages Over Existing System

| Aspect | Existing (SRCNN) | Proposed |
|--------|-----------------|----------|
| Privacy | Raw images sent to cloud | Encrypted before transmission |
| Security | Partially attackable | Enhanced SKK + smoothing |
| DNN Models | SRCNN (super-resolution only) | DenseNet-121 + XceptionNet (diagnosis) |
| Smoothing | None | Median / Mean / Max / Min filters |
| Medical Application | Image quality improvement | Privacy-preserving diagnosis |

---

## Hardware & Software Requirements

**Hardware:** Intel i3+, 2GB RAM, 250GB HDD
**Software:** Python 3.x, MySQL, TensorFlow, OpenCV, Flask, Windows 7+

---

## Developed By

**Afreen** — [GitHub Profile](https://github.com/27-Afreen)
