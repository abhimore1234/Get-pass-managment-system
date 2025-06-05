# Get-pass-managment-system

## overview
<br>
Gate Pass Management System is a Python-based application designed to efficiently handle entry and exit of personnel, vehicles, and visitors within an organization or premises. It ensures secure access control by maintaining detailed records of movements while providing an easy-to-use interface for both administrators and users. The system supports multiple user roles, including Security Personnel, Admin, and Visitor.
<br>

## Features
  
###  Real-Time Face Recognition : <br>
* Detects and recognizes faces in real-time using webcam input.
* Matches live faces against a database of pre-encoded face data.
* Automatically switches between In and Out statuses based on previous scan.

###  MySQL Database Integration : <br>
* Stores user information and attendance logs in a MySQL database.
* Efficiently fetches and updates records such as face encodings, status, scan times, etc.
* Prevents duplicate scans within a configurable cooldown period (default: 1 minute).

###  Email Notifications : <br>
* Sends automatic email alerts to users upon successful recognition.
* Notifies the user of status updates (In/Out) with current date and time.
* Secure SMTP integration with support for Gmail.

### GUI Dashboard (Tkinter) : <br>
* User-friendly interface displaying attendance records in a searchable table.
* Live updates and search functionality to filter records by name.
* Refresh button to reload the latest data on demand.

### Modular & Threaded Design : <br>
* Core functionality is modularized for easier maintenance and scalability.
* Runs face recognition in a separate thread to keep the GUI responsive.

### Data Validation & Error Handling : <br>
* Handles corrupted or malformed face encodings gracefully.
Displays warnings and popups for invalid faces or missing webcam access.
Includes logging for debugging and tracing errors.
<br>
## How to Run
<br>
Install all required libraries.
Generate the QR code from Excel.
Then, it will scan the attendance.
<br>
## Example Use Cases
<br>
### 1. Office Gate Pass System : <br>
Automatically logs employee entries and exits via facial recognition.
Sends email notifications to employees confirming their gate status.
Helps HR or security teams monitor in/out times and generate daily reports.

### 2. School or College Attendance : <br>
Teachers or staff can automate student attendance as they enter or leave classrooms.
Parents receive email alerts when their child enters or exits the school campus.
Prevents proxy attendance through secure biometric verification.

### 3. Hostel In/Out Tracking : <br>
Tracks student movement in hostels for safety and regulation compliance.
Warden/admins get real-time records of who’s in or out.
Provides an accurate digital log for audits or emergency situations.

### 4. Lab Access Control : <br>
Restricts access to labs or restricted areas only to registered personnel.
Maintains a record of entry times for lab usage analysis.
Enhances security by detecting unrecognized individuals.

### 5. Secure Facility Monitoring : <br>
Useful in data centers, research labs, or sensitive areas.
Real-time alerts for unauthorized access attempts.
Easily scalable with additional cameras and face records.
