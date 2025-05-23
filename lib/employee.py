from __init__ import CURSOR, CONN
from department import Department

class Employee:
    all = {}

    def __init__(self, name, job_title, department_id, id=None):
        self.id = id
        self.name = name
        self.job_title = job_title
        self.department_id = department_id

    def __repr__(self):
        return f"<Employee {self.id}: {self.name}, {self.job_title}, Department ID: {self.department_id}>"

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        if isinstance(name, str) and name:
            self._name = name
        else:
            raise ValueError("Name must be a non-empty string")

    @property
    def job_title(self):
        return self._job_title

    @job_title.setter
    def job_title(self, job_title):
        if isinstance(job_title, str) and job_title:
            self._job_title = job_title
        else:
            raise ValueError("Job title must be a non-empty string")

    @property
    def department_id(self):
        return self._department_id

    @department_id.setter
    def department_id(self, department_id):
        if isinstance(department_id, int) and Department.find_by_id(department_id):
            self._department_id = department_id
        else:
            raise ValueError("department_id must reference a department in the database")

    @classmethod
    def create_table(cls):
        sql = """
            CREATE TABLE IF NOT EXISTS employees (
            id INTEGER PRIMARY KEY,
            name TEXT,
            job_title TEXT,
            department_id INTEGER,
            FOREIGN KEY (department_id) REFERENCES departments(id))
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        CURSOR.execute("DROP TABLE IF EXISTS employees")
        CONN.commit()

    def save(self):
        sql = "INSERT INTO employees (name, job_title, department_id) VALUES (?, ?, ?)"
        CURSOR.execute(sql, (self.name, self.job_title, self.department_id))
        CONN.commit()
        self.id = CURSOR.lastrowid
        type(self).all[self.id] = self

    def update(self):
        sql = "UPDATE employees SET name = ?, job_title = ?, department_id = ? WHERE id = ?"
        CURSOR.execute(sql, (self.name, self.job_title, self.department_id, self.id))
        CONN.commit()

    def delete(self):
        sql = "DELETE FROM employees WHERE id = ?"
        CURSOR.execute(sql, (self.id,))
        CONN.commit()
        del type(self).all[self.id]
        self.id = None

    @classmethod
    def create(cls, name, job_title, department_id):
        employee = cls(name, job_title, department_id)
        employee.save()
        return employee

    @classmethod
    def instance_from_db(cls, row):
        if row[0] in cls.all:
            instance = cls.all[row[0]]
            instance.name, instance.job_title, instance.department_id = row[1], row[2], row[3]
        else:
            instance = cls(row[1], row[2], row[3], row[0])
            cls.all[instance.id] = instance
        return instance

    @classmethod
    def get_all(cls):
        rows = CURSOR.execute("SELECT * FROM employees").fetchall()
        return [cls.instance_from_db(row) for row in rows]

    @classmethod
    def find_by_id(cls, id):
        row = CURSOR.execute("SELECT * FROM employees WHERE id = ?", (id,)).fetchone()
        return cls.instance_from_db(row) if row else None

    @classmethod
    def find_by_name(cls, name):
        row = CURSOR.execute("SELECT * FROM employees WHERE name = ?", (name,)).fetchone()
        return cls.instance_from_db(row) if row else None

    def reviews(self):
        from review import Review
        return [r for r in Review.get_all() if r.employee_id == self.id]
