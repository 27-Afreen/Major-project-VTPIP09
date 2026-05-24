# 🏥 VTPIP09 - Medical Imaging & Report System

A web-based medical imaging and report management system built with **Flask** and **MySQL**. It enables patients, doctors, and administrators to interact securely through a role-based portal.

---

## 📸 Screenshots

### 🏠 Home Page
![Home Page](Screenshots/home_page.png)

### 🔐 Login Dashboard
![Login Dashboard](Screenshots/login_dashboard.png)

### 🩺 Doctor Registration
![Doctor Registration](Screenshots/doctor_registration.png)

### 👨‍⚕️ Doctor Dashboard
![Doctor Dashboard](Screenshots/doctor_dashboard.png)

### 🧑 Patient Dashboard
![Patient Dashboard](Screenshots/Patient_dashboard.png)

### 📋 Patient Reports
![Patient Reports](Screenshots/Pt_Reports%20.png)

---

## 🔧 Tech Stack

| Technology | Purpose |
|-----------|---------|
| Python 3 | Backend language |
| Flask | Web framework |
| MySQL | Database |
| OpenCV | Image processing |
| Bootstrap 4 | Frontend styling |
| HTML / Jinja2 | Templating |

---

## 👥 User Roles

### 🔑 Admin
- Login with credentials (`lab` / `lab`)
- View pending scan reports from the lab queue
- Upload processed scan images
- Generate secure access tokens for reports

### 🩺 Doctor
- Register and login with email & password
- View patients who submitted symptoms
- Forward patient cases to the lab for scanning
- View and share completed scan reports with access key

### 🧑 Patient
- Register and login with email & password
- Browse available doctors by department
- Submit symptoms to a chosen doctor
- View scan report using secure access key

---

## ⚙️ Installation & Setup

### 1. Clone the Repository
```bash
git clone https://github.com/27-Afreen/Major-project-VTPIP09.git
cd Major-project-VTPIP09
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Setup MySQL Database
Open MySQL Command Line Client and run:
```sql
SOURCE path/to/vtpip09_2022_setup.sql;
```

### 4. Configure Database in app.py
```python
conn = mysql.connector.connect(
    host="localhost",
    port=3307,            # change to your MySQL port
    user="root",
    password="your_password",
    database="vtpip09_2022"
)
```

### 5. Run the App
```bash
python app.py
```

### 6. Open in Browser
```
http://127.0.0.1:5000
```

---

## 🗄️ Database Tables

| Table | Description |
|-------|-------------|
| `user` | Patient accounts (name, email, password, mobile, location) |
| `doctor` | Doctor accounts (name, email, password, mobile, department) |
| `userdet` | Patient symptom submissions with status tracking |
| `sreport` | Scan reports with secure 10-character access tokens |

---

## 🔄 System Workflow

```
Patient submits symptoms
        ↓
Doctor reviews & forwards to Lab
        ↓
Lab uploads scan image
        ↓
Secure access token generated
        ↓
Doctor & Patient view the scan report
```

---

## 📁 Project Structure

```
spyproject/
├── app.py                    # Main Flask application
├── requirements.txt          # Python dependencies
├── vtpip09_2022_setup.sql    # Database setup script
├── templates/                # 21 HTML templates
│   ├── base.html
│   ├── index.html
│   ├── admin.html / ahome.html
│   ├── doctor.html / dhome.html / dreg.html
│   ├── user.html  / uhome.html / ureg.html
│   └── ... (report & display pages)
├── static/                   # Uploaded scan images
└── Screenshots/              # Project screenshots
```

---

## 🧪 Test Credentials

| Role | Email / Username | Password |
|------|-----------------|----------|
| Admin | `lab` | `lab` |
| Doctor | register first | your password |
| Patient | register first | your password |

---

## 👩‍💻 Developed By

**Afreen** — [GitHub](https://github.com/27-Afreen)
