# ============================================================
# STUDENT PERFORMANCE ANALYSIS SYSTEM
# Developed using Object-Oriented Programming (OOP)
# ============================================================

# Import required Python modules
import csv
from abc import ABC, abstractmethod


# ============================================================
# TASK 2: STUDENT BASE CLASS
# Demonstrates Encapsulation and Abstraction
# ============================================================

class Student(ABC):

    def __init__(self, student_id, first_name, last_name,
                 programme, math, english, science):

        # Encapsulated student information
        self._student_id = student_id
        self._first_name = first_name
        self._last_name = last_name
        self._programme = programme

        # Private dictionary containing subject marks
        self.__marks = {
            "Mathematics": math,
            "English": english,
            "Science": science
        }

        # Validate marks when creating a student
        for subject, mark in self.__marks.items():
            self._validate_mark(mark)

    # Validate individual marks
    @staticmethod
    def _validate_mark(mark):

        if isinstance(mark, bool) or not isinstance(mark, (int, float)):
            raise ValueError("Marks must be numeric.")

        if not 0 <= mark <= 100:
            raise ValueError("Marks must be between 0 and 100.")

    # Properties for accessing student information

    @property
    def student_id(self):
        return self._student_id

    @property
    def first_name(self):
        return self._first_name

    @property
    def last_name(self):
        return self._last_name

    @property
    def programme(self):
        return self._programme

    @property
    def marks(self):
        # Return a copy to protect the original marks
        return self.__marks.copy()

    # Method for updating student marks
    def update_mark(self, subject, new_mark):

        if subject not in self.__marks:
            raise ValueError("Invalid subject.")

        self._validate_mark(new_mark)

        self.__marks[subject] = new_mark

    # Calculate individual student average
    def calculate_average(self):

        total = sum(self.__marks.values())

        return total / len(self.__marks)

    # Determine student grade
    def calculate_grade(self):

        average = self.calculate_average()

        if average >= 80:
            return "A"

        elif average >= 70:
            return "B"

        elif average >= 60:
            return "C"

        elif average >= 50:
            return "D"

        else:
            return "F"

    # Abstract method that subclasses must implement
    @abstractmethod
    def get_student_type(self):
        pass

    # Default scholarship information
    def scholarship_information(self):

        return "Scholarship eligibility not assessed."

    # Generate individual student performance report
    def generate_report(self):

        report = f"""
============================================================
                 STUDENT PERFORMANCE REPORT
============================================================

Student ID: {self.student_id}
Full Name: {self.first_name} {self.last_name}
Programme: {self.programme}
Student Type: {self.get_student_type()}

-------------------- SUBJECT MARKS -------------------------

Mathematics: {self.marks['Mathematics']}
English:     {self.marks['English']}
Science:     {self.marks['Science']}

-------------------- PERFORMANCE ---------------------------

Average Score: {self.calculate_average():.2f}
Grade: {self.calculate_grade()}

---------------- SCHOLARSHIP INFORMATION ------------------

{self.scholarship_information()}

============================================================
"""

        return report


# ============================================================
# TASK 2: AIU STUDENT CLASS
# Demonstrates Inheritance
# ============================================================

class AIUStudent(Student):

    def __init__(self, student_id, first_name, last_name,
                 programme, math, english, science):

        # Call the parent class constructor
        super().__init__(
            student_id,
            first_name,
            last_name,
            programme,
            math,
            english,
            science
        )

    # Implement the abstract method
    def get_student_type(self):

        return "AIU Student"

    # Override the default scholarship information
    def scholarship_information(self):

        return "Not eligible for scholarship."


# ============================================================
# TASK 3: PERFORMANCE ANALYZER CLASS
# Demonstrates Composition
# ============================================================

class PerformanceAnalyzer:

    def __init__(self, students):

        # Store a collection of existing student objects
        self.students = students

    # Find student with the highest average
    def highest_average(self):

        if not self.students:
            raise ValueError("No student records available.")

        return max(
            self.students,
            key=lambda student: student.calculate_average()
        )

    # Find student with the lowest average
    def lowest_average(self):

        if not self.students:
            raise ValueError("No student records available.")

        return min(
            self.students,
            key=lambda student: student.calculate_average()
        )

    # Calculate overall class average
    def class_average(self):

        if not self.students:
            raise ValueError("No student records available.")

        total = sum(
            student.calculate_average()
            for student in self.students
        )

        return total / len(self.students)

    # ========================================================
    # TASK 6: FLEXIBLE METHOD INTERFACE
    # Demonstrates an alternative to Method Overloading
    # ========================================================

    @staticmethod
    def flexible_average(*marks):

        # Accept a list or tuple of marks as well
        if len(marks) == 1 and isinstance(marks[0], (list, tuple)):
            marks = tuple(marks[0])

        if len(marks) == 0:
            raise ValueError("At least one mark is required.")

        for mark in marks:

            Student._validate_mark(mark)

        return sum(marks) / len(marks)


# ============================================================
# TASK 4: SCHOLARSHIP STUDENT CLASS
# Demonstrates Inheritance and Method Overriding
# ============================================================

class ScholarshipStudent(AIUStudent):

    def __init__(self, student_id, first_name, last_name,
                 programme, math, english, science,
                 scholarship_amount):

        # Call the parent class constructor
        super().__init__(
            student_id,
            first_name,
            last_name,
            programme,
            math,
            english,
            science
        )

        self.scholarship_amount = scholarship_amount

    # Check scholarship eligibility
    def is_eligible(self):

        return self.calculate_average() >= 85

    # Override the parent class method
    def get_student_type(self):

        return "Scholarship Student"

    # Override scholarship information
    def scholarship_information(self):

        if self.is_eligible():

            return (
                f"Eligible for scholarship.\n"
                f"Scholarship Amount: KES "
                f"{self.scholarship_amount:,.2f}"
            )

        else:

            return "Not eligible for scholarship."


# ============================================================
# LOAD STUDENT RECORDS FROM CSV FILE
# ============================================================

def load_students(filename):

    students = []

    # Open the CSV file
    with open(filename, "r", newline="", encoding="utf-8") as file:

        reader = csv.DictReader(file)

        # Check that all required columns exist
        required_columns = {
            "StudentID",
            "FName",
            "LName",
            "Programme",
            "Math",
            "English",
            "Science"
        }

        if not required_columns.issubset(reader.fieldnames or []):
            raise ValueError("CSV file is missing required columns.")

        # Read each student record
        for row in reader:

            student_id = row["StudentID"].strip()
            first_name = row["FName"].strip()
            last_name = row["LName"].strip()
            programme = row["Programme"].strip()

            # Convert marks from text to numbers
            math = float(row["Math"])
            english = float(row["English"])
            science = float(row["Science"])

            # Calculate average to determine student type
            average = (math + english + science) / 3

            # Create scholarship student if average is at least 85
            if average >= 85:

                student = ScholarshipStudent(
                    student_id,
                    first_name,
                    last_name,
                    programme,
                    math,
                    english,
                    science,
                    50000
                )

            # Otherwise create an ordinary AIU student
            else:

                student = AIUStudent(
                    student_id,
                    first_name,
                    last_name,
                    programme,
                    math,
                    english,
                    science
                )

            # Add the student object to the collection
            students.append(student)

    if not students:
        raise ValueError("The CSV file contains no student records.")

    return students


# ============================================================
# TASK 7: CLASS PERFORMANCE SUMMARY
# ============================================================

def generate_class_summary(analyzer):

    highest = analyzer.highest_average()
    lowest = analyzer.lowest_average()

    print("\n")
    print("=" * 60)
    print("                 CLASS PERFORMANCE SUMMARY")
    print("=" * 60)

    print(
        f"\nHighest Average: {highest.first_name} "
        f"{highest.last_name} "
        f"({highest.calculate_average():.2f})"
    )

    print(
        f"Lowest Average: {lowest.first_name} "
        f"{lowest.last_name} "
        f"({lowest.calculate_average():.2f})"
    )

    print(
        f"Overall Class Average: {analyzer.class_average():.2f}"
    )

    print(f"Total Students: {len(analyzer.students)}")

    print("=" * 60)


# ============================================================
# TASK 5: POLYMORPHISM DEMONSTRATION
# ============================================================

def demonstrate_polymorphism(students):

    print("\n")
    print("=" * 60)
    print("                 POLYMORPHISM DEMONSTRATION")
    print("=" * 60)

    # Both student types are stored in the same collection
    for student in students:

        print(
            f"{student.first_name} {student.last_name}: "
            f"{student.get_student_type()}"
        )

    print("=" * 60)


# ============================================================
# MAIN PROGRAM
# Runs the complete Student Performance Analysis System
# ============================================================

def main():

    print("\n")
    print("=" * 60)
    print("          STUDENT PERFORMANCE ANALYSIS SYSTEM")
    print("=" * 60)

    # Load students from the CSV dataset
    students = load_students("students.csv")

    print(f"\nSuccessfully loaded {len(students)} student records.")

    # Create the performance analyzer
    analyzer = PerformanceAnalyzer(students)

    # Generate individual student reports
    print("\n")
    print("=" * 60)
    print("                 INDIVIDUAL STUDENT REPORTS")
    print("=" * 60)

    for student in students:

        print(student.generate_report())

    # Display scholarship eligibility
    print("\n")
    print("=" * 60)
    print("                 SCHOLARSHIP ELIGIBILITY")
    print("=" * 60)

    for student in students:

        if isinstance(student, ScholarshipStudent):

            print(
                f"{student.first_name} {student.last_name}: "
                f"{student.is_eligible()} "
                f"- KES {student.scholarship_amount:,.2f}"
            )

        else:

            print(
                f"{student.first_name} {student.last_name}: "
                f"Not eligible"
            )

    # Demonstrate polymorphism
    demonstrate_polymorphism(students)

    # Generate class performance summary
    generate_class_summary(analyzer)

    # Demonstrate flexible method interface
    print("\n")
    print("=" * 60)
    print("              FLEXIBLE INTERFACE DEMONSTRATION")
    print("=" * 60)

    result_one = PerformanceAnalyzer.flexible_average(
        75, 80, 70
    )

    result_two = PerformanceAnalyzer.flexible_average(
        75, 80, 70, 90, 85
    )

    result_three = PerformanceAnalyzer.flexible_average(
        [75, 80, 70]
    )

    print(f"Average of three marks: {result_one:.2f}")
    print(f"Average of five marks: {result_two:.2f}")
    print(f"Average using a list: {result_three:.2f}")

    print("=" * 60)

    print("\nSTUDENT PERFORMANCE ANALYSIS COMPLETED SUCCESSFULLY!")


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":

    try:

        main()

    except FileNotFoundError:

        print("\nERROR: students.csv file was not found.")
        print("Make sure students.csv is in the same folder as main.py.")

    except (ValueError, KeyError) as error:

        print(f"\nERROR: {error}")

    except Exception as error:

        print(f"\nUNEXPECTED ERROR: {error}")
        