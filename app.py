import streamlit as st
import mysql.connector
import pandas as pd

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Rushhour1.",
        database="Project"
    )

st.set_page_config(page_title="Ashesi Hostel Manager", layout="centered")
st.title("Ashesi Hostel Management System")

# Role Selection and Authentication
def authenticate_user(role):
    if "admin_authenticated" not in st.session_state:
        st.session_state.admin_authenticated = False

    manager_id = None
    student_id = None

    if role == "Hostel Manager":
        manager_id = st.sidebar.text_input("Enter Your Manager ID")

    elif role == "Student":
        student_id = st.sidebar.text_input("Enter Your Student ID")
        if student_id:
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT 1 FROM Student WHERE StudentID = %s", (student_id,))
            result = cursor.fetchone()
            conn.close()

            if not result:
                st.error("❌ Invalid Student ID. Please check your ID.")
                student_id = None  # Invalidate the student_id

    elif role == "Administrator":
        st.sidebar.write("### Admin Login")
        admin_id = st.sidebar.text_input("Admin ID", key="admin_id_input")
        admin_password = st.sidebar.text_input("Password", type="password", key="admin_pass_input")
        if st.sidebar.button("Login"):
            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Administration WHERE AdminID = %s AND admin_password = %s", (admin_id, admin_password))
            if cursor.fetchone():
                st.success("✅ Logged in as Administrator")
                st.session_state.admin_authenticated = True
                st.session_state.admin_id = admin_id
            else:
                st.error("❌ Invalid Admin credentials")
            conn.close()

    return manager_id, student_id, st.session_state.admin_authenticated

role = st.sidebar.selectbox("Select Your Role", ["Administrator", "Hostel Manager", "Student"])
manager_id, student_id, admin_authenticated = authenticate_user(role)

# Fetch hostel_id early for hostel managers
hostel_id = None
if role == "Hostel Manager" and manager_id:
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT Hostel_id FROM Hostel_Manager WHERE ManagerId = %s", (manager_id,))
    result = cursor.fetchone()
    if result:
        hostel_id = result[0]
    else:
        st.warning("⚠️ Invalid Manager ID or no assigned hostel.")
    conn.close()


# Menu options based on role
def get_menu(role, authenticated):
    if role == "Administrator" and authenticated:
        return [
            "Dashboard",
            "Manage Students",
            "Manage Payments",
            "Manage Maintenance Reports",
            "View Room Assignments",
            "View Roommate Preferences"
        ]
    elif role == "Hostel Manager":
        return [
            "Dashboard",
            "Manage Payments",
            "Manage Maintenance Reports",
            "View Room Assignments",
            "View Roommate Preferences"
        ]
    elif role == "Student":
        return [
            "Dashboard",
            "View My Maintenance Reports",
            "Submit Maintenance Report",
            "View My Room Assignment",
            "View My Payment Status",
            "Make a Payment",
            "Submit/Update Roommate Preference"
        ]
    else:
        return []

menu = get_menu(role, admin_authenticated)
choice = st.sidebar.selectbox("Select Operation", menu) if menu else None

# DASHBOARD VIEW
if choice == "Dashboard":
    conn = connect_db()
    cursor = conn.cursor()

    if role == "Administrator" and admin_authenticated:
        cursor.execute("SELECT COUNT(*) FROM Student")
        total_students = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM Payment")
        total_payments = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM Payment WHERE payment_status = 'Overdue'")
        overdue_payments = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM Reports")
        total_reports = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM Reports WHERE report_status = 'Pending'")
        pending_reports = cursor.fetchone()[0]

        col1, col2 = st.columns(2)
        with col1:
            st.metric("👨‍🎓 Total Students", total_students)
            st.metric("📨 Overdue Payments", overdue_payments)
        with col2:
            st.metric("💰 Total Payments", total_payments)
            st.metric("🛠 Pending Reports", pending_reports)

    elif role == "Hostel Manager" and manager_id:
        if hostel_id:
            # NOW do the dashboard counts for this hostel manager:
            cursor.execute("SELECT COUNT(*) FROM Reports WHERE Hostel_id = %s", (hostel_id,))
            total_reports = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM Reports WHERE report_status = 'Pending' AND Hostel_id = %s", (hostel_id,))
            pending_reports = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM Payment WHERE Hostel_id = %s", (hostel_id,))
            total_payments = cursor.fetchone()[0]

            cursor.execute("SELECT COUNT(*) FROM Payment WHERE payment_status = 'Overdue' AND Hostel_id = %s", (hostel_id,))
            overdue_payments = cursor.fetchone()[0]

            col1, col2 = st.columns(2)
            with col1:
                st.metric("📄 Total Reports for Your Hostel", total_reports)
                st.metric("💸 Overdue Payments", overdue_payments)
            with col2:
                st.metric("🛠 Pending Reports", pending_reports)
                st.metric("💰 Payments Recorded", total_payments)

        else:
            st.warning("⚠️ You have no assigned hostel.")


    elif role == "Student" and student_id:
        cursor.execute("SELECT COUNT(*) FROM Reports WHERE Student_id = %s", (student_id,))
        my_reports = cursor.fetchone()[0]

        cursor.execute("SELECT COUNT(*) FROM Payment WHERE Student_id = %s AND payment_status = 'Overdue'", (student_id,))
        my_overdue = cursor.fetchone()[0]

        st.metric("📄 My Maintenance Reports", my_reports)
        st.metric("💸 My Overdue Payments", my_overdue)

    conn.close()

# STEP 2: Filtered Manage Payments logic will be added below this in the next step


# Manage Students
if choice == "Manage Students":
    st.subheader("🎓 Student Management")

    sub_option = st.selectbox("Choose a student task:", [
        "Register a New Student",
        "View All Students",
        "Search Student by ID"
    ])

    conn = connect_db()
    cursor = conn.cursor()

    if sub_option == "Register a New Student":
        student_id = st.text_input("Student ID")
        first_name = st.text_input("First Name")
        last_name = st.text_input("Last Name")
        gender = st.selectbox("Gender", ["Male", "Female", "Other"])
        year = st.selectbox("Graduating Year", [2024, 2025, 2026, 2027, 2028])
        scholarship = st.selectbox("Scholarship Status", ["Yes", "No", "Partial"])

        if st.button("Register"):
            query = """
                INSERT INTO Student (StudentID, StudentFirstName, StudentLastName, Gender, YearGroup, Scholarship_Status)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (student_id, first_name, last_name, gender, year, scholarship)

            try:
                cursor.execute(query, values)
                conn.commit()
                st.success(f"✅ {first_name} {last_name} has been registered successfully!")
            except Exception as e:
                st.error(f"❌ Failed to insert student: {e}")

    elif sub_option == "View All Students":
        query = """
            SELECT 
                StudentID, 
                CONCAT(StudentFirstName, ' ', StudentLastName) AS FullName, 
                Gender, 
                YearGroup, 
                Scholarship_Status
            FROM Student
        """
        cursor.execute(query)
        results = cursor.fetchall()
        df = pd.DataFrame(results, columns=["Student ID", "Full Name", "Gender", "Year Group", "Scholarship Status"])
        st.dataframe(df, use_container_width=True)

    elif sub_option == "Search Student by ID":
        search_id = st.text_input("Enter Student ID")
        if st.button("Search"):
            query = """
                SELECT 
                    StudentID, 
                    StudentFirstName, 
                    StudentLastName, 
                    Gender, 
                    YearGroup, 
                    Scholarship_Status
                FROM Student 
                WHERE StudentID = %s
            """
            cursor.execute(query, (search_id,))
            result = cursor.fetchone()
            if result:
                df = pd.DataFrame([result], columns=["Student ID", "First Name", "Last Name", "Gender", "Year Group", "Scholarship Status"])
                st.dataframe(df, use_container_width=True)
            else:
                st.warning("No student found with that ID.")

    conn.close()

# Manage Payments
if choice == "Manage Payments":
    st.subheader("💰 Payment Management")

    if role == "Administrator" and admin_authenticated:
        sub_option = st.selectbox("Choose a payment task:", [
            "View All Payments",
            "View Overdue Payments",
            "Students Without Payment",
            "Delete Payments for Scholarship Students"
        ])
    elif role == "Hostel Manager":
        sub_option = st.selectbox("Choose a payment task:", [
            "View All Payments",
            "View Overdue Payments"
        ])

    conn = connect_db()
    cursor = conn.cursor()

    if role == "Administrator" and admin_authenticated:
        filter_clause = ""
        filter_value = ()
    elif role == "Hostel Manager" and manager_id:
        cursor.execute("SELECT Hostel_id FROM Hostel_Manager WHERE ManagerId = %s", (manager_id,))
        result = cursor.fetchone()
        if result:
            hostel_id = result[0]
            filter_clause = "WHERE Hostel.HostelID = %s"
            filter_value = (hostel_id,)
        else:
            st.warning("Invalid Manager ID or no assigned hostel")
            conn.close()
            st.stop()
    else:
        st.warning("Only Admins and Hostel Managers can manage payments from this menu")
        conn.close()
        st.stop()

    if sub_option == "View All Payments":
        query = f"""
            SELECT 
                CONCAT(Student.StudentFirstName, ' ', Student.StudentLastName) AS StudentName,
                Hostel.HostelName, 
                Payment.Amount, 
                Payment.payment_status
            FROM Student
            INNER JOIN Payment ON Student.StudentID = Payment.Student_id
            INNER JOIN Hostel ON Hostel.HostelID = Payment.Hostel_id
            {filter_clause}
        """
        cursor.execute(query, filter_value)
        results = cursor.fetchall()
        df = pd.DataFrame(results, columns=["Student", "Hostel", "Amount", "Status"])
        st.dataframe(df, use_container_width=True)

    elif sub_option == "View Overdue Payments":
        query = f"""
            SELECT 
                CONCAT(Student.StudentFirstName, ' ', Student.StudentLastName) AS StudentName,
                Hostel.HostelName, 
                Payment.Amount, 
                Payment.payment_status
            FROM Student
            INNER JOIN Payment ON Student.StudentID = Payment.Student_id
            INNER JOIN Hostel ON Hostel.HostelID = Payment.Hostel_id
            WHERE Payment.payment_status = 'Overdue' AND Payment.Amount > 0
            {"AND Hostel.HostelID = %s" if role == 'Hostel Manager' else ""}
            ORDER BY Payment.Amount DESC
        """
        cursor.execute(query, filter_value)
        results = cursor.fetchall()
        df = pd.DataFrame(results, columns=["Student", "Hostel", "Amount", "Status"])
        st.dataframe(df, use_container_width=True)

    elif sub_option == "Students Without Payment" and role == "Administrator" and admin_authenticated:
        query = """
            SELECT 
                CONCAT(StudentFirstName, ' ', StudentLastName) AS StudentName
            FROM Student
            LEFT JOIN Payment ON Student.StudentID = Payment.Student_id
            WHERE Payment.Student_id IS NULL
            ORDER BY StudentName
        """
        cursor.execute(query)
        results = cursor.fetchall()
        df = pd.DataFrame(results, columns=["Student Name"])
        st.dataframe(df, use_container_width=True)

    elif sub_option == "Delete Payments for Scholarship Students" and role == "Administrator" and admin_authenticated:
        if st.button("Delete All"):
            query = """
                DELETE FROM Payment
                WHERE Student_id IN (
                    SELECT StudentID FROM Student WHERE Scholarship_Status != 'No'
                )
            """
            try:
                cursor.execute(query)
                conn.commit()
                st.success("✅ Payments for scholarship students deleted successfully!")
            except Exception as e:
                st.error(f"❌ Failed to delete: {e}")

    conn.close()


    
# STEP 3: Manage Maintenance Reports
if choice == "Manage Maintenance Reports":
    st.subheader("🛠️ Maintenance Reports")

    conn = connect_db()
    cursor = conn.cursor()

    if role == "Administrator" and admin_authenticated:
        sub_option = st.selectbox("Choose a maintenance task:", [
            "Submit New Report",
            "View All Reports",
            "View Reports by Status",
            "View Reports by Hostel",
            "Delete a Report"
        ])
    elif role == "Hostel Manager":
        sub_option = st.selectbox("Choose a maintenance task:", [
            "View All Reports for My Hostel",
            "View Reports by Status",
            "Delete a Report"
        ])
    elif role == "Student":
        sub_option = choice  # student has separate top-level options

    # ADMIN AND MANAGER SHARED VIEWS
    if (role in ["Administrator", "Hostel Manager"] and (admin_authenticated or manager_id)):

        if sub_option == "View All Reports" or sub_option == "View All Reports for My Hostel":
            filter_clause = "" if role == "Administrator" else "WHERE Reports.Hostel_id = %s"
            filter_value = () if role == "Administrator" else (hostel_id,)

            query = f"""
                SELECT 
                    Reports.ReportID,
                    CONCAT(Student.StudentFirstName, ' ', Student.StudentLastName) AS StudentName,
                    Hostel.HostelName,
                    Reports.type_of_report,
                    Reports.Descr,
                    Reports.report_status
                FROM Reports
                JOIN Student ON Reports.Student_id = Student.StudentID
                JOIN Hostel ON Reports.Hostel_id = Hostel.HostelID
                {filter_clause}
                ORDER BY Reports.ReportID
            """
            cursor.execute(query, filter_value)
            results = cursor.fetchall()
            df = pd.DataFrame(results, columns=["Report ID", "Student", "Hostel", "Type", "Description", "Status"])
            st.dataframe(df, use_container_width=True)

        elif sub_option == "View Reports by Status":
            selected_status = st.selectbox("Choose status:", ["Pending", "Resolved", "Investigating"])
            query = f"""
                SELECT 
                    Reports.ReportID,
                    CONCAT(Student.StudentFirstName, ' ', Student.StudentLastName) AS StudentName,
                    Hostel.HostelName,
                    Reports.type_of_report,
                    Reports.Descr
                FROM Reports
                JOIN Student ON Reports.Student_id = Student.StudentID
                JOIN Hostel ON Reports.Hostel_id = Hostel.HostelID
                WHERE Reports.report_status = %s
                {"AND Reports.Hostel_id = %s" if role == 'Hostel Manager' else ""}
            """
            values = (selected_status,) if role == "Administrator" else (selected_status, hostel_id)
            cursor.execute(query, values)
            results = cursor.fetchall()
            df = pd.DataFrame(results, columns=["Report ID", "Student", "Hostel", "Type", "Description"])
            st.dataframe(df, use_container_width=True)

        elif sub_option == "View Reports by Hostel":
            hostel_id_input = st.text_input("Enter Hostel ID to filter reports")

            if st.button("Search Reports"):
                query = """
                    SELECT 
                        Reports.ReportID,
                        CONCAT(Student.StudentFirstName, ' ', Student.StudentLastName) AS StudentName,
                        Hostel.HostelName,
                        Reports.type_of_report,
                        Reports.Descr,
                        Reports.report_status
                    FROM Reports
                    JOIN Student ON Reports.Student_id = Student.StudentID
                    JOIN Hostel ON Reports.Hostel_id = Hostel.HostelID
                    WHERE Reports.Hostel_id = %s
                """
                cursor.execute(query, (hostel_id_input,))
                results = cursor.fetchall()
                if results:
                    df = pd.DataFrame(results, columns=["Report ID", "Student", "Hostel", "Type", "Description", "Status"])
                    st.dataframe(df, use_container_width=True)
                else:
                    st.warning("No reports found for this hostel.")

        elif sub_option == "Delete a Report":
            report_id = st.text_input("Enter Report ID to delete")
            if st.button("Delete Report"):
                query = "DELETE FROM Reports WHERE ReportID = %s"
                try:
                    cursor.execute(query, (report_id,))
                    conn.commit()
                    st.success("✅ Report deleted successfully!")
                except Exception as e:
                    st.error(f"❌ Failed to delete report: {e}")



    # ADMIN AND STUDENT SUBMIT
    if (role == "Administrator" and sub_option == "Submit New Report") or (role == "Student" and sub_option == "Submit Maintenance Report"):
        st.write("### 📝 Submit a Maintenance Report")
        report_id = st.text_input("Report ID")
        sid = student_id if role == "Student" else st.text_input("Student ID")
        hid = st.text_input("Hostel ID")
        report_type = st.selectbox("Type of Report", ["Maintenance", "Complaint", "Emergency", "Electricity", "Other"])
        description = st.text_area("Description")
        status = st.selectbox("Report Status", ["Pending", "Resolved", "Investigating"])

        if st.button("Submit Report"):
            query = """
                INSERT INTO Reports (ReportID, type_of_report, Descr, report_status, Student_id, Hostel_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (report_id, report_type, description, status, sid, hid)
            try:
                cursor.execute(query, values)
                conn.commit()
                st.success("✅ Report submitted successfully!")
            except Exception as e:
                st.error(f"❌ Failed to submit report: {e}")

    # STUDENT VIEW
    if role == "Student" and sub_option == "View My Maintenance Reports" and student_id:
        query = """
            SELECT 
                Reports.ReportID,
                Reports.type_of_report,
                Reports.Descr,
                Reports.report_status
            FROM Reports
            WHERE Reports.Student_id = %s
        """
        cursor.execute(query, (student_id,))
        results = cursor.fetchall()
        df = pd.DataFrame(results, columns=["Report ID", "Type", "Description", "Status"])
        st.dataframe(df, use_container_width=True)

    conn.close()


#STEP 4: View Room Assignments
if choice == "View Room Assignments" or choice == "View My Room Assignment":
    st.subheader("🛏️ Room Assignments")

    conn = connect_db()
    cursor = conn.cursor()

    if role == "Administrator" and admin_authenticated:
        sub_option = st.selectbox("Choose a room assignment task:", [
            "View All Room Assignments",
            "View Students in a Specific Room",
            "Find Fully Occupied Rooms"
        ])

        if sub_option == "View All Room Assignments":
            query = """
                SELECT 
                    Student.StudentID,
                    CONCAT(Student.StudentFirstName, ' ', Student.StudentLastName) AS StudentName,
                    Hostel.HostelName,
                    Room.Room_No
                FROM Booking
                JOIN Student ON Booking.Student_id = Student.StudentID
                JOIN Room ON Booking.Room_id = Room.RoomID
                JOIN Hostel ON Room.Hostel_id = Hostel.HostelID
            """
            cursor.execute(query)
            results = cursor.fetchall()
            df = pd.DataFrame(results, columns=["Student ID", "Student Name", "Hostel", "Room Number"])
            st.dataframe(df, use_container_width=True)

        elif sub_option == "View Students in a Specific Room":
            room_id = st.text_input("Enter Room ID")
            if st.button("Search"):
                query = """
                    SELECT Student.StudentID, CONCAT(Student.StudentFirstName, ' ', Student.StudentLastName) AS StudentName
                    FROM Booking
                    JOIN Student ON Booking.Student_id = Student.StudentID
                    WHERE Booking.Room_id = %s
                """
                cursor.execute(query, (room_id,))
                results = cursor.fetchall()
                if results:
                    df = pd.DataFrame(results, columns=["Student ID", "Student Name"])
                    st.dataframe(df, use_container_width=True)
                else:
                    st.warning("No students found for the specified room ID.")

        elif sub_option == "Find Fully Occupied Rooms":
            query = """
                SELECT Room.RoomID, Room.Room_No
                FROM Room
                JOIN Booking ON Room.RoomID = Booking.Room_id
                GROUP BY Room.RoomID, Room.Room_No, Room.num_of_occupants, Room.max_occupants
                HAVING COUNT(Booking.Student_id) = Room.max_occupants
            """
            cursor.execute(query)
            results = cursor.fetchall()
            df = pd.DataFrame(results, columns=["Room ID", "Room Number"])
            st.dataframe(df, use_container_width=True)

    elif role == "Hostel Manager" and manager_id:
        cursor.execute("SELECT Hostel_id FROM Hostel_Manager WHERE ManagerId = %s", (manager_id,))
        result = cursor.fetchone()
        if result:
            hostel_id = result[0]
            query = """
                SELECT 
                    Student.StudentID,
                    CONCAT(Student.StudentFirstName, ' ', Student.StudentLastName) AS StudentName,
                    Room.Room_No
                FROM Booking
                JOIN Student ON Booking.Student_id = Student.StudentID
                JOIN Room ON Booking.Room_id = Room.RoomID
                WHERE Room.Hostel_id = %s
            """
            cursor.execute(query, (hostel_id,))
            results = cursor.fetchall()
            df = pd.DataFrame(results, columns=["Student ID", "Student Name", "Room Number"])
            st.dataframe(df, use_container_width=True)
        else:
            st.warning("⚠️ Invalid Manager ID or no assigned hostel.")

    elif role == "Student":
        st.write(f"Student ID detected: {student_id}")  # DEBUG LINE
        if not student_id:
            st.warning("Student ID not provided. Please login properly.")
        else:
            query = """
                SELECT 
                    Hostel.HostelName,
                    Room.Room_No
                FROM Booking
                JOIN Room ON Booking.Room_id = Room.RoomID
                JOIN Hostel ON Room.Hostel_id = Hostel.HostelID
                WHERE Booking.Student_id = %s
            """
            cursor.execute(query, (student_id,))
            result = cursor.fetchone()
            st.write(f"Query Result: {result}")  # DEBUG LINE

            if result:
                hostel_name, room_no = result
                st.success(f"You are assigned to {hostel_name}, Room {room_no}.")
            else:
                st.info("No room assignment found for this student. Contact administration if needed.")



    conn.close()

# STEP 5: Student Payment & Report Submission Features
if role == "Student" and student_id:
    conn = connect_db()
    cursor = conn.cursor()

    if choice == "View My Payment Status":
        query = """
            SELECT Hostel.HostelName, Payment.Amount, Payment.payment_status, Payment.payment_date
            FROM Payment
            JOIN Hostel ON Payment.Hostel_id = Hostel.HostelID
            WHERE Payment.Student_id = %s
        """
        cursor.execute(query, (student_id,))
        results = cursor.fetchall()
        if results:
            df = pd.DataFrame(results, columns=["Hostel", "Amount", "Status", "Date"])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No payment records found.")

    elif choice == "Make a Payment":
        st.subheader("💳 Make a Payment")
        payment_id = st.text_input("Payment ID")
        amount = st.number_input("Amount", min_value=0)
        hostel_id_input = st.text_input("Hostel ID")

        if st.button("Submit Payment"):
            query = """
                INSERT INTO Payment (PaymentID, Amount, payment_status, payment_date, Student_id, Hostel_id)
                VALUES (%s, %s, 'Pending', CURDATE(), %s, %s)
            """
            values = (payment_id, amount, student_id, hostel_id_input)
            try:
                cursor.execute(query, values)
                conn.commit()
                st.success("✅ Payment submitted successfully!")
            except Exception as e:
                st.error(f"❌ Failed to submit payment: {e}")

    elif choice == "Submit Maintenance Report":
        st.subheader("📝 Submit a Maintenance Report")
        report_id = st.text_input("Report ID")
        hostel_id = st.text_input("Hostel ID")
        report_type = st.selectbox("Type of Report", ["Maintenance", "Complaint", "Emergency", "Electricity", "Other"])
        description = st.text_area("Description")
        status = st.selectbox("Report Status", ["Pending", "Resolved", "Investigating"])

        if st.button("Submit Report"):
            query = """
                INSERT INTO Reports (ReportID, type_of_report, Descr, report_status, Student_id, Hostel_id)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (report_id, report_type, description, status, student_id, hostel_id)
            try:
                cursor.execute(query, values)
                conn.commit()
                st.success("✅ Report submitted successfully!")
            except Exception as e:
                st.error(f"❌ Failed to submit report: {e}")

    elif choice == "View My Maintenance Reports":
        query = """
            SELECT ReportID, type_of_report, Descr, report_status
            FROM Reports
            WHERE Student_id = %s
        """
        cursor.execute(query, (student_id,))
        results = cursor.fetchall()
        if results:
            df = pd.DataFrame(results, columns=["Report ID", "Type", "Description", "Status"])
            st.dataframe(df, use_container_width=True)
        else:
            st.info("No maintenance reports found.")

    conn.close()

if role == "Student" and student_id and choice == "Submit/Update Roommate Preference":
    st.subheader("📝 Submit or Update Your Roommate Preferences")

    study_pref = st.selectbox("Preferred Study Habit", ["Quiet", "Soft Music", "Group Study"])
    social_pref = st.selectbox("Social Habit", ["Introvert", "Extrovert", "Ambivert"])
    noise_pref = st.selectbox("Preferred Noise Level", ["Quiet", "Moderate", "Lively"])
    preferred_roommate = st.text_input("Preferred Roommate ID (optional)")

    if st.button("Submit"):
        conn = connect_db()
        cursor = conn.cursor()

        # First check if preference already exists
        cursor.execute("SELECT * FROM Roommate_Preference WHERE student_id = %s", (student_id,))
        exists = cursor.fetchone()

        if exists:
            # Update existing
            query = """
                UPDATE Roommate_Preference
                SET study_preference = %s, social_preference = %s, noise_level = %s, preferred_roommate_id = %s
                WHERE student_id = %s
            """
            values = (study_pref, social_pref, noise_pref, preferred_roommate if preferred_roommate else None, student_id)
        else:
            # Insert new
            query = """
                INSERT INTO Roommate_Preference (Preference_id, student_id, study_preference, social_preference, noise_level, preferred_roommate_id)
                VALUES (UUID_SHORT(), %s, %s, %s, %s, %s)
            """
            values = (student_id, study_pref, social_pref, noise_pref, preferred_roommate if preferred_roommate else None)

        try:
            cursor.execute(query, values)
            conn.commit()
            st.success("✅ Preferences saved successfully!")
        except Exception as e:
            st.error(f"❌ Failed to save preferences: {e}")

        conn.close()

if (role == "Administrator" and admin_authenticated) or (role == "Hostel Manager" and manager_id):
    if choice == "View Roommate Preferences":
        st.subheader("👥 Roommate Preferences")

        conn = connect_db()
        cursor = conn.cursor()

        if role == "Administrator" and admin_authenticated:
            query = """
                SELECT 
                    Student.StudentID,
                    CONCAT(Student.StudentFirstName, ' ', Student.StudentLastName) AS FullName,
                    study_preference,
                    social_preference,
                    noise_level,
                    preferred_roommate_id
                FROM Roommate_Preference
                JOIN Student ON Roommate_Preference.student_id = Student.StudentID
            """
            cursor.execute(query)
        
        elif role == "Hostel Manager" and manager_id:
            query = """
                SELECT 
                    Student.StudentID,
                    CONCAT(Student.StudentFirstName, ' ', Student.StudentLastName) AS FullName,
                    Roommate_Preference.study_preference,
                    Roommate_Preference.social_preference,
                    Roommate_Preference.noise_level,
                    Roommate_Preference.preferred_roommate_id
                FROM Roommate_Preference
                JOIN Student ON Roommate_Preference.student_id = Student.StudentID
                JOIN Booking ON Student.StudentID = Booking.Student_id
                JOIN Room ON Booking.Room_id = Room.RoomID
                WHERE Room.Hostel_id = %s
            """
            cursor.execute(query, (hostel_id,))

        results = cursor.fetchall()

        df = pd.DataFrame(results, columns=["Student ID", "Name", "Study Preference", "Social Habit", "Noise Level", "Preferred Roommate ID"])
        st.dataframe(df, use_container_width=True)

        conn.close()
