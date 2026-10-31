import sys
import pandas as pd
import os

from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHeaderView

# ---------------- BASE PATH ----------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

STUDENT_FILE = os.path.join(BASE_DIR, "students.csv")
ADMIN_FILE = os.path.join(BASE_DIR, "admin.csv")

# ---------------- COURSE SEMESTER MAP ----------------
COURSE_SEMESTERS = {
    "BTECH": 8,
    "BCA": 6,
    "BSC": 6,
    "BCOM": 6
}

# ---------------- INIT FILES ----------------
def init_files():
    if not os.path.exists(STUDENT_FILE):
        pd.DataFrame(columns=[
            "RegNo","Name","Course",
            "Fees Paid","Fees Pending",
            "Total Fees",
            "Sem1","Sem2","Sem3","Sem4","Sem5","Sem6","Sem7","Sem8"
        ]).to_csv(STUDENT_FILE, index=False)


    if not os.path.exists(ADMIN_FILE):
        pd.DataFrame([{"Username":"admin","Password":"1234"}]).to_csv(ADMIN_FILE, index=False)


# ---------------- SIGNUP ----------------
class Signup(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Create Admin")
        self.resize(300, 200)

        layout = QVBoxLayout()

        self.user = QLineEdit()
        self.user.setPlaceholderText("Username")

        self.passw = QLineEdit()
        self.passw.setPlaceholderText("Password")
        self.passw.setEchoMode(QLineEdit.Password)

        btn = QPushButton("Create")
        btn.clicked.connect(self.create_admin)

        layout.addWidget(QLabel("Create Admin"))
        layout.addWidget(self.user)
        layout.addWidget(self.passw)
        layout.addWidget(btn)

        self.setLayout(layout)

    def create_admin(self):
        df = pd.read_csv(ADMIN_FILE)

        u = self.user.text().strip()
        p = self.passw.text().strip()

        if not u or not p:
            QMessageBox.warning(self, "Error", "Fill all fields")
            return

        if u in df["Username"].astype(str).values:
            QMessageBox.warning(self, "Error", "User exists")
            return

        df.loc[len(df)] = [u, p]
        df.to_csv(ADMIN_FILE, index=False)

        QMessageBox.information(self, "Success", "Admin Created")
        self.close()


# ---------------- LOGIN ----------------
class Login(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login")
        self.resize(300, 250)

        layout = QVBoxLayout()

        self.user = QLineEdit()
        self.user.setPlaceholderText("Username")

        self.passw = QLineEdit()
        self.passw.setPlaceholderText("Password")
        self.passw.setEchoMode(QLineEdit.Password)

        login_btn = QPushButton("Login")
        signup_btn = QPushButton("Create Admin")

        login_btn.clicked.connect(self.check_login)
        signup_btn.clicked.connect(self.open_signup)

        layout.addWidget(QLabel("Admin Login"))
        layout.addWidget(self.user)
        layout.addWidget(self.passw)
        layout.addWidget(login_btn)
        layout.addWidget(signup_btn)

        self.setLayout(layout)

    def check_login(self):
        df = pd.read_csv(ADMIN_FILE)

        df["Username"] = df["Username"].astype(str).str.strip()
        df["Password"] = df["Password"].astype(str).str.strip()

        u = self.user.text().strip()
        p = self.passw.text().strip()

        if not df[(df["Username"] == u) & (df["Password"] == p)].empty:
            self.close()
            self.main = Dashboard()
            self.main.show()
        else:
            QMessageBox.warning(self, "Error", "Invalid Login")

    def open_signup(self):
        self.signup = Signup()
        self.signup.show()


# ---------------- DASHBOARD ----------------
class Dashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dashboard")
        self.resize(1000, 600)

        layout = QVBoxLayout()

        btn_layout = QHBoxLayout()

        btn1 = QPushButton("Students")
        

        btn1.clicked.connect(self.show_students)
       

        btn_layout.addWidget(btn1)
       

        self.stack = QStackedWidget()

        self.student_page = StudentPage()
        

        self.stack.addWidget(self.student_page)

        layout.addLayout(btn_layout)
        layout.addWidget(self.stack)

        self.setLayout(layout)

    def show_students(self):
        self.stack.setCurrentWidget(self.student_page)




# ---------------- STUDENT PAGE (DYNAMIC) ----------------
class StudentPage(QWidget):
    def __init__(self):
        super().__init__()

        self.df = pd.read_csv(STUDENT_FILE)

        layout = QVBoxLayout()
        form = QGridLayout()

        self.reg = QLineEdit()
        self.name = QLineEdit()
        self.course = QComboBox()
        self.course.addItems(COURSE_SEMESTERS.keys())
        self.course.currentTextChanged.connect(self.generate_semesters)
        self.fees_paid = QLineEdit()
        self.fees_pending = QLineEdit()

        self.sem_inputs = []

        labels = [
            "RegNo","Name","Course",
            "Fees Paid","Fees Pending"
        ]

        self.fields = [
            self.reg,self.name,self.course,
            self.fees_paid,self.fees_pending
        ]

        for i,(l,w) in enumerate(zip(labels,self.fields)):
            form.addWidget(QLabel(l), i, 0)
            form.addWidget(w, i, 1)

        self.sem_container = QVBoxLayout()
        form.addWidget(QLabel("Sem CGPA"), 5, 0)
        form.addLayout(self.sem_container, 5, 1)

        layout.addLayout(form)

        # BUTTONS
        btns = QHBoxLayout()

        add = QPushButton("Add")
        delete = QPushButton("Delete")
        update = QPushButton("Update")

        add.clicked.connect(self.add_student)
        delete.clicked.connect(self.delete_student)
        update.clicked.connect(self.update_student)

        btns.addWidget(add)
        btns.addWidget(delete)
        btns.addWidget(update)

        layout.addLayout(btns)

        # SEARCH
        self.search = QLineEdit()
        self.search.setPlaceholderText("Search by RegNo or Name")
        self.search.textChanged.connect(self.search_data)
        layout.addWidget(self.search)

        # TABLE
        self.table = QTableWidget()
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        self.setLayout(layout)

        self.load_table()
        self.table.cellClicked.connect(self.select_row)
        self.generate_semesters()

    # ---------------- SEM GENERATION ----------------
    def generate_semesters(self):
        course = self.course.currentText().strip().upper()

        count = COURSE_SEMESTERS.get(course, 6)

        # clear old
        for i in reversed(range(self.sem_container.count())):
            widget = self.sem_container.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        self.sem_inputs = []

        for i in range(count):
            inp = QLineEdit()
            inp.setPlaceholderText(f"Sem {i+1} CGPA (0-10)")
            inp.setText("0")  # NEW STUDENT DEFAULT ZERO
            self.sem_inputs.append(inp)
            self.sem_container.addWidget(inp)

    # ---------------- LOAD ----------------
    def load_table(self, data=None):
        if data is None:
            data = self.df

        self.table.setRowCount(len(data))
        self.table.setColumnCount(len(data.columns))

        self.table.setHorizontalHeaderLabels(data.columns)

        for i in range(len(data)):
            for j,val in enumerate(data.iloc[i]):
                self.table.setItem(i,j,QTableWidgetItem(str(val)))

    # ---------------- ADD ----------------
    def add_student(self):
        try:
            if not self.reg.text() or not self.name.text():
                QMessageBox.warning(self, "Error", "RegNo and Name required")
                return 
            if self.reg.text() in self.df["RegNo"].astype(str).values:
                QMessageBox.warning(self, "Error", "RegNo already exists")
                return

            paid = float(self.fees_paid.text() or 0)
            pending = float(self.fees_pending.text() or 0)
            total = paid + pending

            sem_marks = []
            for s in self.sem_inputs:
                val = float(s.text() or 0)
                if val < 0 or val > 10:
                    raise ValueError("CGPA must be between 0 and 10")
                sem_marks.append(val)
            
            while len(sem_marks) < 8:
                sem_marks.append(0)
                
            new = [
                self.reg.text(),
                self.name.text(),
                self.course.currentText(),
                paid,
                pending,
                total
            ] + sem_marks

            self.df.loc[len(self.df)] = new
            self.df.to_csv(STUDENT_FILE, index=False)
            self.df = pd.read_csv(STUDENT_FILE)
            self.load_table()
            self.reg.clear()
            self.name.clear()
            self.fees_paid.clear()
            self.fees_pending.clear()
            self.generate_semesters()
        
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))
        
    # ---------------- DELETE ----------------
    def delete_student(self):
        row = self.table.currentRow()
        if row < 0:
            return

        reg = self.table.item(row,0).text()
        self.df = self.df[self.df["RegNo"] != reg]
        self.df.to_csv(STUDENT_FILE, index=False)
        self.df = pd.read_csv(STUDENT_FILE)
        self.load_table()

    # ---------------- UPDATE ----------------
    def update_student(self):
        row = self.table.currentRow()
        if row < 0:
            return

        try:
            reg = self.reg.text()
            if not reg or not self.name.text():
                QMessageBox.warning(self, "Error", "RegNo and Name required")
                return

            if reg not in self.df["RegNo"].astype(str).values:
                QMessageBox.warning(self, "Error", "RegNo not found")
                return

            paid = float(self.fees_paid.text() or 0)
            pending = float(self.fees_pending.text() or 0)
            total = paid + pending

            sem_marks = []
            for s in self.sem_inputs:
                val = float(s.text() or 0)
                if val < 0 or val > 10:
                    raise ValueError("CGPA must be between 0 and 10")
                sem_marks.append(val)
            
            while len(sem_marks) < 8:
                sem_marks.append(0)
            self.df.loc[self.df["RegNo"] == reg] = [
                reg,
                self.name.text(),
                self.course.currentText(),
                paid,
                pending,
                total
            ] + sem_marks

            self.df.to_csv(STUDENT_FILE, index=False)
            self.df = pd.read_csv(STUDENT_FILE)
            self.load_table()

        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))

    # ---------------- SEARCH ----------------
    def search_data(self):
        key = self.search.text().lower()

        if key == "":
            self.load_table(self.df)
            return

        filtered = self.df[
            self.df["RegNo"].astype(str).str.lower().str.contains(key) |
            self.df["Name"].astype(str).str.lower().str.contains(key)
        ]

        self.load_table(filtered)

    # ---------------- SELECT ----------------
    def select_row(self,row,col):
        for i, w in enumerate(self.fields):
            value = self.table.item(row, i).text()

            if isinstance(w, QComboBox):
                w.setCurrentText(value)
            else:
                w.setText(value)
        for i, sem in enumerate(self.sem_inputs):
            item = self.table.item(row, 6 + i)
            if item:
                sem.setText(item.text())

# ---------------- RUN ----------------
init_files()

app = QApplication(sys.argv)
login = Login()
login.show()
sys.exit(app.exec())