import cv2
import face_recognition
import numpy as np
import mysql.connector
import pickle
import tkinter as tk
from tkinter import messagebox, ttk
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import threading
import traceback
# Email Configuration
EMAIL_SENDER = "abhi027446@gmail.com"  # Replace with your email
EMAIL_PASSWORD = "sdkv cbtd zfxp woud"  # Replace with your email password
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587


# MySQL Connection
def create_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="face_record"
    )

# Fetch face encodings from the database
def fetch_face_encodings():
    conn = create_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, face_encoding, email, category, mobile_number FROM person_records")
    face_data = cursor.fetchall()
    conn.close()

    ids, encodings, names, emails, categories, mobile_numbers = [], [], [], [], [], []
    for row in face_data:
        id, name, encoding_blob, email, category, mobile_number = row
        try:
            encoding = pickle.loads(encoding_blob)
            if len(encoding) != 128:
                print(f"Warning: Encoding for {name} is incorrect. Skipping.")
                continue
            ids.append(id)
            encodings.append(encoding)
            names.append(name)
            emails.append(email)
            categories.append(category)
            mobile_numbers.append(mobile_number)
        except Exception as e:
            print(f"Error decoding face encoding for {name}: {e}")
            continue

    print(f"✅ Loaded {len(encodings)} face encodings from database.")
    return ids, encodings, names, emails, categories, mobile_numbers

# Get last scan time and status
def get_last_scan_time(name):
    conn = create_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT status, last_scan_time FROM person_records WHERE name = %s", (name,))
    result = cursor.fetchone()
    conn.close()
    if result:
        last_scan_time = result[1]
        return result[0], last_scan_time if last_scan_time else None
    return None, None

# Update status and last scan time
def update_status(name, status):
    conn = create_db_connection()
    cursor = conn.cursor()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("UPDATE person_records SET status = %s, last_scan_time = %s WHERE name = %s",
                   (status, current_time, name))
    conn.commit()
    conn.close()

# Mark attendance in the database
def mark_attendance(name, email, category, status, tree):
    conn = create_db_connection()
    cursor = conn.cursor()
    time_now = datetime.now().strftime("%H:%M:%S")
    date_now = datetime.now().strftime("%Y-%m-%d")
    
    # Fetch mobile number from the person_records table
    cursor.execute("SELECT mobile_number FROM person_records WHERE name = %s", (name,))
    result = cursor.fetchone()
    mobile_number = result[0] if result else "N/A"  # Default to "N/A" if mobile number is not found

    cursor.execute(
        "INSERT INTO attendance (name, mobile_number, email, status, category, date, time) VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (name, mobile_number, email, status, category, date_now, time_now)
    )
    conn.commit()
    conn.close()

    # Refresh the Treeview to show the new data
    display_attendance_data(tree)

# Function to send an email notification
def send_email(to_email, name, status):
    # Get the current date and time
    current_time = datetime.now().strftime("%H:%M:%S")
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Email subject and message
    subject = "Face Recognition Attendance System"
    message = (
        f"Hello {name},\n\n"
        f"Your attendance status has been updated to: {status}.\n"
        f"Date: {current_date}\n"
        f"Time: {current_time}\n\n"
        "Best Regards,\n"
        "Attendance System"
    )

    try:
        print(f"📧 Attempting to send email to {to_email} for {name} ({status})...")
        
        # Create the email
        msg = MIMEMultipart()
        msg["From"] = EMAIL_SENDER
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(message, "plain"))

        # Connect to the SMTP server and send the email
        server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        server.sendmail(EMAIL_SENDER, to_email, msg.as_string())
        server.quit()

        print(f"✅ Email sent successfully to {to_email}")
        
        # Show a popup message for successful email sending
        messagebox.showinfo("Email Sent", f"Email sent successfully to {to_email}")
    
    except smtplib.SMTPException as e:
        print(f"❌ Email sending failed: {e}")
        messagebox.showerror("Email Failed", f"Failed to send email: {e}")

# Face recognition function
def recognize_faces(ids_known, encodings_known, names_known, emails_known, categories_known, mobile_numbers_known, tree):
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("❌ Error: Could not access the camera.")
            messagebox.showerror("Camera Error", "Could not access the camera. Please check your webcam.")
            return

        print("📷 Starting video capture... Press 'q' to exit.")

        while True:
            success, img = cap.read()
            if not success:
                print("❌ Error: Failed to capture image")
                messagebox.showerror("Capture Error", "Failed to capture image from camera.")
                break  # Exit loop if frame capture fails

            try:
                img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                faces_in_frame = face_recognition.face_locations(img_rgb)
                encodes_in_frame = face_recognition.face_encodings(img_rgb, faces_in_frame)

                if not faces_in_frame:
                    print("⚠ Warning: No faces detected.")
                    continue  # Skip processing if no face is found

                for encode_face, face_location in zip(encodes_in_frame, faces_in_frame):
                    top, right, bottom, left = face_location

                    matches = face_recognition.compare_faces(encodings_known, encode_face, tolerance=0.65)
                    face_distances = face_recognition.face_distance(encodings_known, encode_face)
                    best_match_index = np.argmin(face_distances) if len(face_distances) > 0 else -1

                    if best_match_index != -1 and matches[best_match_index]:
                        id = ids_known[best_match_index]
                        name = names_known[best_match_index]
                        email = emails_known[best_match_index]
                        category = categories_known[best_match_index]
                        mobile_number = mobile_numbers_known[best_match_index]

                        current_status, last_scan_time = get_last_scan_time(name)

                        # Prevent duplicate scans within 1 minute
                        if last_scan_time and datetime.now() - last_scan_time < timedelta(minutes=1):
                            print(f"⏳ Skipping {name}, scanned too recently.")
                            continue

                        new_status = "Out" if current_status == "In" else "In"
                        update_status(name, new_status)
                        mark_attendance(name, email, category, new_status, tree)  
                        send_email(email, name, new_status)

                        status_text = f"{name} ({new_status})"
                        color = (0, 255, 0) if new_status == "In" else (0, 0, 255)
                    else:
                        status_text = "Invalid Face"
                        color = (0, 0, 255)
                        print("❌ Warning: Invalid Face Detected")
                        messagebox.showwarning("Invalid Face", "Unknown face detected!")

                    cv2.rectangle(img, (left, top), (right, bottom), color, 2)
                    cv2.putText(img, status_text, (left, bottom + 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)

                cv2.imshow('Face Recognition', img)

            except Exception as e:
                print(f"❌ Error processing frame: {e}")
                traceback.print_exc()

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    except Exception as e:
        print(f"❌ Critical Error in Face Recognition: {e}")
        traceback.print_exc()
        messagebox.showerror("Critical Error", f"An error occurred: {e}")

    finally:
        print("🛑 Stopping video capture...")
        cap.release()
        cv2.destroyAllWindows()


# Start recognition
def start_face_recognition(tree):
    ids_known, encodings_known, names_known, emails_known, categories_known, mobile_numbers_known = fetch_face_encodings()
    if len(encodings_known) == 0:
        print("No face encodings found in database.")
        return
    recognize_faces(ids_known, encodings_known, names_known, emails_known, categories_known, mobile_numbers_known, tree)

# Fetch attendance records
def fetch_attendance_data():
    conn = create_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, name, mobile_number, status, category, date, time FROM attendance ORDER BY date DESC, time DESC")
    data = cursor.fetchall()
    conn.close()
    
    # Debug: Print fetched data
    print("Fetched Data:", data)
    return data

# Show temporary "Data not found" popup
def show_temp_popup(message):
    popup = tk.Toplevel()
    popup.title("Search Result")
    popup.geometry("250x100")
    popup.resizable(False, False)
    tk.Label(popup, text=message, font=("Arial", 12)).pack(pady=20)
    popup.after(2000, popup.destroy)  # Close after 2 seconds

# Display attendance data in the Treeview
def display_attendance_data(tree, search_query=""):
    # Clear existing data
    for row in tree.get_children():
        tree.delete(row)

    # Fetch attendance data
    attendance_data = fetch_attendance_data()

    # Filter data based on search query
    filtered_data = [record for record in attendance_data if search_query.lower() in record[1].lower()] if search_query else attendance_data

    # Reverse the data to show the most recent at the bottom
    filtered_data = filtered_data[::-1]

    # Show "Data not found" popup if no records match
    if not filtered_data:
        show_temp_popup("Data not found")

    # Insert filtered data into Treeview
    for record in filtered_data:
        # Debug: Print each record being inserted
        print("Inserting Record:", record)
        tree.insert("", "end", values=record)  # Insert the entire record (including id)

# Handle search on 'Enter' key press
def on_search(event, tree, search_entry):
    search_query = search_entry.get().strip()
    display_attendance_data(tree, search_query)

def refresh_data(tree):
    display_attendance_data(tree)
    messagebox.showinfo("Refresh", "Data has been refreshed.")

# GUI setup
def create_gui():
    gui_window = tk.Tk()
    gui_window.title("Attendance System")
    gui_window.geometry("800x500")

    tk.Label(gui_window, text="Face Recognition Attendance System", font=("Arial", 14)).pack(pady=10)

    search_frame = tk.Frame(gui_window)
    search_frame.pack(pady=5)
    
    tk.Label(search_frame, text="Search Name:", font=("Arial", 12)).pack(side="left", padx=5)
    search_entry = tk.Entry(search_frame, font=("Arial", 12), width=30)
    search_entry.pack(side="left", padx=5)

    refresh_button = tk.Button(search_frame, text="Refresh", font=("Arial", 12), command=lambda: refresh_data(tree))
    refresh_button.pack(side="left", padx=5)

    columns = ("ID", "Name", "Mobile Number", "Status", "Category", "Date", "Time")
    tree = ttk.Treeview(gui_window, columns=columns, show="headings", height=15)
    
    # Set column headings
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=120, anchor="center")

    tree.pack(pady=10, fill="both", expand=True)

    # Load initial data
    display_attendance_data(tree)

    # Bind search function to 'Enter' key
    search_entry.bind("<Return>", lambda event: on_search(event, tree, search_entry))

    # Run face recognition in a separate thread to avoid blocking the GUI
    face_recognition_thread = threading.Thread(target=start_face_recognition, args=(tree,), daemon=True)
    face_recognition_thread.start()

    gui_window.mainloop()

# ...existing code...

# Run GUI
if __name__ == "__main__":
    create_gui()
