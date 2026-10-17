
import sqlite3
import tkinter as tk
from pathlib import Path
from tkinter import ttk, messagebox

try:
    import mysql.connector
    from mysql.connector import Error as MySQLDBError
except ImportError:
    mysql = None
    MySQLDBError = RuntimeError

# =====================================================
# DATABASE CONFIGURATION
# =====================================================
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "pass@123",  # Change if required
}
DATABASE = "OnlineEducationDB"
DB_PATH = Path(__file__).with_name("online_education.db")


def create_connection():
    if mysql is not None:
        try:
            return mysql.connector.connect(**DB_CONFIG, database=DATABASE)
        except Exception:
            pass

    try:
        conn = sqlite3.connect(str(DB_PATH))
        conn.execute("PRAGMA foreign_keys = ON")
        return conn
    except sqlite3.Error:
        return None


def setup_database():
    if mysql is not None:
        try:
            conn = mysql.connector.connect(**DB_CONFIG)
            cursor = conn.cursor()
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DATABASE}")
            cursor.close()
            conn.close()
        except Exception:
            pass

    conn = create_connection()
    if not conn:
        raise RuntimeError("Could not connect to the database.")

    cursor = conn.cursor()

    statements = [
        """
        CREATE TABLE IF NOT EXISTS INSTRUCTOR (
            I_ID INT PRIMARY KEY,
            I_NAME VARCHAR(100) NOT NULL,
            I_TYPE VARCHAR(30) NOT NULL,
            I_EMAIL VARCHAR(150) UNIQUE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS TEACHING (
            I_ID INT PRIMARY KEY,
            T_TYPE VARCHAR(50),
            FOREIGN KEY (I_ID) REFERENCES INSTRUCTOR(I_ID)
            ON DELETE CASCADE ON UPDATE CASCADE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS NON_TEACHING (
            I_ID INT PRIMARY KEY,
            T_TYPE VARCHAR(50),
            FOREIGN KEY (I_ID) REFERENCES INSTRUCTOR(I_ID)
            ON DELETE CASCADE ON UPDATE CASCADE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS STUDENT (
            ST_ID INT PRIMARY KEY,
            ST_NAME VARCHAR(100) NOT NULL,
            ST_EMAIL VARCHAR(150) UNIQUE,
            ST_COURSE VARCHAR(100)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS GRADES (
            G_NO INT PRIMARY KEY,
            G_SCORE DECIMAL(5,2) NOT NULL,
            I_ID INT,
            FOREIGN KEY (I_ID) REFERENCES INSTRUCTOR(I_ID)
            ON DELETE SET NULL ON UPDATE CASCADE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS ASSESSMENT (
            A_ID INT PRIMARY KEY,
            A_MARKS DECIMAL(5,2) NOT NULL,
            A_TYPE VARCHAR(50)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS GRADE_ASSESSMENT (
            G_NO INT,
            A_ID INT,
            PRIMARY KEY (G_NO, A_ID),
            FOREIGN KEY (G_NO) REFERENCES GRADES(G_NO)
            ON DELETE CASCADE ON UPDATE CASCADE,
            FOREIGN KEY (A_ID) REFERENCES ASSESSMENT(A_ID)
            ON DELETE CASCADE ON UPDATE CASCADE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS SUBMISSION (
            SU_ID INT PRIMARY KEY,
            SU_TIMESTAMP DATETIME DEFAULT CURRENT_TIMESTAMP,
            SU_DATE DATE NOT NULL,
            ST_ID INT NOT NULL,
            A_ID INT NOT NULL,
            FOREIGN KEY (ST_ID) REFERENCES STUDENT(ST_ID)
            ON DELETE CASCADE ON UPDATE CASCADE,
            FOREIGN KEY (A_ID) REFERENCES ASSESSMENT(A_ID)
            ON DELETE CASCADE ON UPDATE CASCADE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS FEES (
            F_NO INT PRIMARY KEY,
            F_AMOUNT DECIMAL(10,2) NOT NULL,
            ST_ID INT NOT NULL,
            FOREIGN KEY (ST_ID) REFERENCES STUDENT(ST_ID)
            ON DELETE CASCADE ON UPDATE CASCADE
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS RECEIPT (
            R_NO INT PRIMARY KEY,
            R_DATE DATE NOT NULL,
            R_COURSE VARCHAR(100),
            ST_ID INT NOT NULL,
            UNIQUE (ST_ID, R_NO),
            FOREIGN KEY (ST_ID) REFERENCES STUDENT(ST_ID)
            ON DELETE CASCADE ON UPDATE CASCADE
        )
        """
    ]

    try:
        for sql in statements:
            cursor.execute(sql)
        conn.commit()
    finally:
        cursor.close()
        conn.close()


# =====================================================
# TABLE DEFINITIONS FOR THE GUI
# =====================================================
TABLES = {
    "INSTRUCTOR": [
        "I_ID", "I_NAME", "I_TYPE", "I_EMAIL"
    ],
    "TEACHING": [
        "I_ID", "T_TYPE"
    ],
    "NON_TEACHING": [
        "I_ID", "T_TYPE"
    ],
    "STUDENT": [
        "ST_ID", "ST_NAME", "ST_EMAIL", "ST_COURSE"
    ],
    "GRADES": [
        "G_NO", "G_SCORE", "I_ID"
    ],
    "ASSESSMENT": [
        "A_ID", "A_MARKS", "A_TYPE"
    ],
    "GRADE_ASSESSMENT": [
        "G_NO", "A_ID"
    ],
    "SUBMISSION": [
        "SU_ID", "SU_TIMESTAMP", "SU_DATE", "ST_ID", "A_ID"
    ],
    "FEES": [
        "F_NO", "F_AMOUNT", "ST_ID"
    ],
    "RECEIPT": [
        "R_NO", "R_DATE", "R_COURSE", "ST_ID"
    ]
}

PRIMARY_KEYS = {
    "INSTRUCTOR": ["I_ID"],
    "TEACHING": ["I_ID"],
    "NON_TEACHING": ["I_ID"],
    "STUDENT": ["ST_ID"],
    "GRADES": ["G_NO"],
    "ASSESSMENT": ["A_ID"],
    "GRADE_ASSESSMENT": ["G_NO", "A_ID"],
    "SUBMISSION": ["SU_ID"],
    "FEES": ["F_NO"],
    "RECEIPT": ["R_NO"]
}


# =====================================================
# MAIN APPLICATION
# =====================================================
class OnlineEducationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Online Education Management System")
        self.root.geometry("1050x650")
        self.root.configure(bg="#EEF3F8")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Treeview",
            rowheight=27,
            font=("Arial", 10)
        )
        style.configure(
            "Treeview.Heading",
            font=("Arial", 10, "bold")
        )

        header = tk.Frame(root, bg="#17365D", height=80)
        header.pack(fill="x")
        header.pack_propagate(False)

        tk.Label(
            header,
            text="ONLINE EDUCATION SYSTEM",
            bg="#17365D",
            fg="white",
            font=("Arial", 21, "bold")
        ).pack(pady=22)

        tk.Label(
            root,
            text="Select an entity to manage its database records",
            bg="#EEF3F8",
            fg="#17365D",
            font=("Arial", 14)
        ).pack(pady=14)

        # Dashboard statistics
        stats = tk.Frame(root, bg="#EEF3F8")
        stats.pack(fill="x", padx=20)

        self.stat_labels = {}

        for name in ["STUDENT", "INSTRUCTOR",
                     "ASSESSMENT", "SUBMISSION"]:
            card = tk.Frame(
                stats, bg="white",
                highlightbackground="#CBD5E1",
                highlightthickness=1
            )
            card.pack(
                side="left", expand=True,
                fill="x", padx=5, pady=5
            )

            tk.Label(
                card, text=name,
                bg="white", fg="#52657A",
                font=("Arial", 10, "bold")
            ).pack(pady=(12, 4))

            value = tk.Label(
                card, text="0",
                bg="white", fg="#17365D",
                font=("Arial", 22, "bold")
            )
            value.pack(pady=(0, 12))
            self.stat_labels[name] = value

        # Entity management buttons
        button_frame = tk.Frame(root, bg="#EEF3F8")
        button_frame.pack(
            fill="both", expand=True, padx=30, pady=20
        )

        for index, table in enumerate(TABLES):
            button = tk.Button(
                button_frame,
                text="Manage " + table.replace("_", " "),
                command=lambda t=table: self.manage_table(t),
                bg="#2874A6",
                fg="white",
                activebackground="#1B4F72",
                activeforeground="white",
                font=("Arial", 10, "bold"),
                width=22,
                height=2,
                relief="flat",
                cursor="hand2"
            )
            button.grid(
                row=index // 3,
                column=index % 3,
                padx=8, pady=7,
                sticky="nsew"
            )

        for col in range(3):
            button_frame.columnconfigure(col, weight=1)

        ttk.Button(
            root, text="Refresh Dashboard",
            command=self.refresh_dashboard
        ).pack(pady=(0, 15))

        self.refresh_dashboard()

    # =================================================
    # DATABASE OPERATIONS
    # =================================================
    def execute_query(self, sql, params=(), fetch=False):
        conn = create_connection()
        if not conn:
            return None

        cursor = None
        try:
            if isinstance(conn, sqlite3.Connection):
                sql = sql.replace("%s", "?")
            cursor = conn.cursor()
            cursor.execute(sql, params)

            if fetch:
                return cursor.fetchall()

            conn.commit()
            return cursor.rowcount

        except Exception as e:
            try:
                conn.rollback()
            except Exception:
                pass
            messagebox.showerror("SQL Error", str(e))
            return None

        finally:
            if cursor:
                cursor.close()
            conn.close()

    def refresh_dashboard(self):
        for table in self.stat_labels:
            rows = self.execute_query(
                f"SELECT COUNT(*) FROM {table}",
                fetch=True
            )
            if rows is not None:
                self.stat_labels[table].config(text=str(rows[0][0]))

    # =================================================
    # TABLE MANAGEMENT WINDOW
    # =================================================
    def manage_table(self, table):
        columns = TABLES[table]

        win = tk.Toplevel(self.root)
        win.title("Manage " + table)
        win.geometry("1050x650")
        win.minsize(800, 450)

        tk.Label(
            win, text=table.replace("_", " ") + " MANAGEMENT",
            font=("Arial", 17, "bold"),
            fg="#17365D"
        ).pack(pady=12)

        # Table
        tree_frame = ttk.Frame(win)
        tree_frame.pack(
            fill="both", expand=True, padx=12, pady=8
        )

        tree = ttk.Treeview(
            tree_frame, columns=columns,
            show="headings", selectmode="browse"
        )

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150, minwidth=90)

        y_scroll = ttk.Scrollbar(
            tree_frame, orient="vertical",
            command=tree.yview
        )
        x_scroll = ttk.Scrollbar(
            tree_frame, orient="horizontal",
            command=tree.xview
        )

        tree.configure(
            yscrollcommand=y_scroll.set,
            xscrollcommand=x_scroll.set
        )

        tree.grid(row=0, column=0, sticky="nsew")
        y_scroll.grid(row=0, column=1, sticky="ns")
        x_scroll.grid(row=1, column=0, sticky="ew")

        tree_frame.rowconfigure(0, weight=1)
        tree_frame.columnconfigure(0, weight=1)

        # Form
        form = ttk.LabelFrame(
            win, text="Record Details", padding=10
        )
        form.pack(fill="x", padx=12, pady=5)

        entries = {}

        for index, col in enumerate(columns):
            row = index // 3
            pos = (index % 3) * 2

            ttk.Label(form, text=col).grid(
                row=row, column=pos,
                padx=5, pady=5, sticky="w"
            )

            entry = ttk.Entry(form, width=23)
            entry.grid(
                row=row, column=pos + 1,
                padx=5, pady=5, sticky="ew"
            )
            entries[col] = entry

        for col in range(6):
            form.columnconfigure(col, weight=1)

        selected = {"values": None}

        def clear_form():
            selected["values"] = None
            for entry in entries.values():
                entry.delete(0, tk.END)

        def selected_record(event=None):
            selection = tree.selection()
            if not selection:
                return

            values = tree.item(selection[0], "values")
            selected["values"] = values

            for col, value in zip(columns, values):
                entries[col].delete(0, tk.END)
                entries[col].insert(0, str(value))

        tree.bind("<<TreeviewSelect>>", selected_record)

        def load_data():
            for item in tree.get_children():
                tree.delete(item)

            sql = f"SELECT * FROM {table} ORDER BY " + ", ".join(
                f"`{key}`" for key in PRIMARY_KEYS[table]
            )

            rows = self.execute_query(sql, fetch=True)

            if rows is not None:
                for row in rows:
                    tree.insert(
                        "", "end",
                        values=[
                            "" if v is None else str(v)
                            for v in row
                        ]
                    )

        def insert_record():
            values = [
                entries[col].get().strip()
                for col in columns
            ]

            # Allow the database to set the timestamp automatically.
            if table == "SUBMISSION" and not values[1]:
                insert_columns = [
                    c for c in columns if c != "SU_TIMESTAMP"
                ]
                values = [
                    entries[c].get().strip()
                    for c in insert_columns
                ]
            else:
                insert_columns = columns[:]

            if any(v == "" for v in values):
                messagebox.showwarning(
                    "Missing Fields",
                    "Fill all required fields. "
                    "For an automatic submission timestamp, "
                    "leave SU_TIMESTAMP blank."
                )
                return

            placeholders = ", ".join(["%s"] * len(values))
            col_sql = ", ".join(
                f"`{c}`" for c in insert_columns
            )

            result = self.execute_query(
                f"INSERT INTO {table} ({col_sql}) "
                f"VALUES ({placeholders})",
                tuple(values)
            )

            if result is not None:
                messagebox.showinfo(
                    "Success", "Record inserted successfully."
                )
                load_data()
                clear_form()
                self.refresh_dashboard()

        def update_record():
            if not selected["values"]:
                messagebox.showwarning(
                    "Select Record",
                    "Select a row from the table first."
                )
                return

            values = [
                entries[col].get().strip()
                for col in columns
            ]

            keys = PRIMARY_KEYS[table]
            non_keys = [c for c in columns if c not in keys]

            if any(
                not entries[c].get().strip()
                for c in non_keys
            ):
                messagebox.showwarning(
                    "Missing Fields",
                    "Fill all non-key fields before updating."
                )
                return

            assignments = ", ".join(
                f"`{col}`=%s" for col in non_keys
            )
            where = " AND ".join(
                f"`{key}`=%s" for key in keys
            )

            params = tuple(
                entries[c].get().strip() for c in non_keys
            ) + tuple(
                selected["values"][columns.index(k)]
                for k in keys
            )

            result = self.execute_query(
                f"UPDATE {table} SET {assignments} WHERE {where}",
                params
            )

            if result is not None:
                messagebox.showinfo(
                    "Success", "Update operation completed."
                )
                load_data()
                clear_form()
                self.refresh_dashboard()

        def delete_record():
            if not tree.selection():
                messagebox.showwarning(
                    "Select Record",
                    "Select a row to delete."
                )
                return

            record = tree.item(
                tree.selection()[0], "values"
            )
            keys = PRIMARY_KEYS[table]

            if not messagebox.askyesno(
                "Confirm Delete",
                "Delete the selected record?\n"
                "Related records may also be deleted "
                "because of foreign-key cascade rules."
            ):
                return

            where = " AND ".join(
                f"`{key}`=%s" for key in keys
            )
            params = tuple(
                record[columns.index(key)] for key in keys
            )

            result = self.execute_query(
                f"DELETE FROM {table} WHERE {where}",
                params
            )

            if result is not None:
                messagebox.showinfo(
                    "Success", "Delete operation completed."
                )
                load_data()
                clear_form()
                self.refresh_dashboard()

        def retrieve_record():
            if not tree.selection():
                messagebox.showwarning(
                    "Select Record",
                    "Select a row to retrieve."
                )
                return

            record = tree.item(
                tree.selection()[0], "values"
            )

            details = "\n".join(
                f"{col}: {val}"
                for col, val in zip(columns, record)
            )

            messagebox.showinfo("Record Details", details)

        # Action buttons
        action_frame = ttk.Frame(win)
        action_frame.pack(fill="x", padx=12, pady=12)

        ttk.Button(
            action_frame, text="Insert",
            command=insert_record
        ).pack(side="left", padx=5)

        ttk.Button(
            action_frame, text="Update",
            command=update_record
        ).pack(side="left", padx=5)

        ttk.Button(
            action_frame, text="Delete",
            command=delete_record
        ).pack(side="left", padx=5)

        ttk.Button(
            action_frame, text="Retrieve",
            command=retrieve_record
        ).pack(side="left", padx=5)

        ttk.Button(
            action_frame, text="Clear Form",
            command=clear_form
        ).pack(side="left", padx=5)

        load_data()


# =====================================================
# RUN APPLICATION
# =====================================================
if __name__ == "__main__":
    try:
        setup_database()
        root = tk.Tk()
        app = OnlineEducationApp(root)
        root.mainloop()
    except Exception as e:
        messagebox.showerror(
            "Startup Error",
            f"Unable to start application:\n{e}"
        )
