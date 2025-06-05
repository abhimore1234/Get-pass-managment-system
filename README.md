# Get-pass-managment-system

## overview
<br>
Gate Pass Management System is a Python-based application designed to efficiently handle entry and exit of personnel, vehicles, and visitors within an organization or premises. It ensures secure access control by maintaining detailed records of movements while providing an easy-to-use interface for both administrators and users. The system supports multiple user roles, including Security Personnel, Admin, and Visitor.
<br>

## Features
  
*  Real-Time Face Recognition : <br>
Detects and recognizes faces in real-time using webcam input.
Matches live faces against a database of pre-encoded face data.
Automatically switches between In and Out statuses based on previous scan.

*  MySQL Database Integration : <br>
Stores user information and attendance logs in a MySQL database.
Efficiently fetches and updates records such as face encodings, status, scan times, etc.
Prevents duplicate scans within a configurable cooldown period (default: 1 minute).

*  Email Notifications : <br>
Sends automatic email alerts to users upon successful recognition.
Notifies the user of status updates (In/Out) with current date and time.
Secure SMTP integration with support for Gmail.

* GUI Dashboard (Tkinter) : <br>
User-friendly interface displaying attendance records in a searchable table.
Live updates and search functionality to filter records by name.
Refresh button to reload the latest data on demand.

* Modular & Threaded Design : <br>
Core functionality is modularized for easier maintenance and scalability.
Runs face recognition in a separate thread to keep the GUI responsive.

* Data Validation & Error Handling : <br>
Handles corrupted or malformed face encodings gracefully.
Displays warnings and popups for invalid faces or missing webcam access.
Includes logging for debugging and tracing errors.
