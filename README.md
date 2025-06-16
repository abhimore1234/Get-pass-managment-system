# 🚪 Gate Pass Management System
A Python-based solution for efficient entry and exit tracking within an organization. Designed to enhance security, streamline visitor management, and maintain detailed movement records.

## 📌 Overview
<br>
Gate Pass Management System enables secure access control by leveraging facial recognition, database integration, and email notifications. Multiple user roles—Security Personnel, Admin, and Visitor—ensure an organized workflow
<br>

## 🎯Features
  
### ✅ Real-Time Face Recognition
- 🚀 Instantly detects and recognizes faces using webcam input.
- 🔍 Matches scanned faces against a secure database of registered users.
- 🔄 Auto-switches between "In" and "Out" based on previous scan status.


### 📊 MySQL Database Integration : <br>
- Stores user information and attendance logs in a MySQL database.
- Efficiently fetches and updates records such as face encodings, status, scan times, etc.
- Prevents duplicate scans within a configurable cooldown period (default: 1 minute).

###  ✉️ Automated Email Notifications
 <br>
- Users receive instant email updates on entry/exit status with timestamps.
- Sends automatic email alerts to users upon successful recognition.
- Notifies the user of status updates (In/Out) with current date and time.
- Secure SMTP integration with support for Gmail.

### 🖥️ GUI Dashboard (Tkinter)
- 📌 Live attendance tracking with a searchable table.
- 🔄 Refresh button for quick updates.
- 📊 User-friendly interface for security monitoring.
### 🔧 Modular & Threaded Design
- 📂 Core functionality is modularized for easy maintenance.
- 🚀 Face recognition runs in a separate thread to keep the GUI responsive.
### ⚠️ Data Validation & Error Handling
- 🛠️ Gracefully handles corrupted or missing face encodings.
- 🚨 Displays warnings for invalid faces or missing webcam access.
- 📝 Debug logs help trace errors effectively.

## 🚀 How to Run
1️⃣ Install all required dependencies<br>
2️⃣ Generate the QR code from Excel<br>
3️⃣ Run the system to scan attendance automatically

## 🔍 Example Use Cases
### 🏢 Office Gate Pass System
- ✅ Automatically logs employee entries/exits via facial recognition.
- 📬 Sends email notifications to employees confirming gate status.
- 📊 Helps HR & security teams track movement patterns.
### 🎓 School & College Attendance
- 👩‍🏫 Teachers automate student attendance as they enter/leave classrooms.
- 👪 Parents receive entry/exit alerts for their children.
- 🚫 Prevents proxy attendance with biometric verification.
### 🏠 Hostel In/Out Tracking
- 🏫 Monitors student movement for security and compliance.
- 📜 Admins get real-time access records.
- 📊 Ensures accurate digital logs for audits or emergencies.
### 🏗️ Lab Access Control
- 🔐 Restricts lab entry to authorized personnel.
- 📜 Maintains entry timestamps for security and usage tracking.
- 🛑 Detects unauthorized individuals instantly.
### 🏭 Secure Facility Monitoring
- 🔍 Useful in data centers, research labs, and sensitive areas.
- 🚨 Sends real-time alerts for unauthorized access attempts.
- 🔄 Easily scalable with additional cameras & face records.


