import sqlite3

DB = None
CONN = None

######### Queries########
def get_student_by_github(github):
    try:
        query = """SELECT first_name, last_name, github FROM Students WHERE github = ?"""
        DB.execute(query, (github,))
        row = DB.fetchone()
        print """\
    Student: %s %s
    Github account: %s"""%(row[0], row[1], row[2])
    except:
        print "That's not a handle I have in my database. \nTo add this student/user, use the new_student command."


def get_projects_by_title(title):
    try:
        query = """SELECT title, description, max_grade FROM Projects WHERE title = ?"""
        DB.execute(query, (title,))
        row = DB.fetchone()
        print """\
    Title: %s
    Description: %s
    Max Grade: %d""" %(row[0],row[1],row[2])
        return True
    except:
        print "Project does not exist. Try again!"
        return False


def get_grade_by_student_project(first_name,last_name,project):
    try:
        query = """SELECT grade FROM Grades 
        INNER JOIN Students 
        ON student_github = github 
        WHERE first_name = ? 
        AND last_name =? AND project_title = ?"""
        DB.execute(query, (first_name,last_name,project))
        row = DB.fetchone()
        print """\
    First Name: %s
    Last Name: %s
    Project: %s
    Grade: %d""" %(first_name, last_name, project,row[0])
    except:
        print "I couldn't match this info. You're gonna have to try again."

def grades_by_student(first_name,last_name):
    try:
        query = """SELECT project_title, grade FROM Grades WHERE
        student_github = 
        (SELECT github FROM Students WHERE first_name = ? and last_name = ?)"""
        DB.execute(query, (first_name,last_name))
        row = DB.fetchall()
        print "For %s %s:" %(first_name,last_name)
        for card in row:
            print "Project: %s - Grade: %d" %(card[0],card[1])
    except:
        print "I can't find records for this student. Try again. "    



######### Data Entry #########
def make_new_student(first_name,last_name,github):
    query = """INSERT into Students values (?,?,?)"""
    DB.execute(query, (first_name, last_name, github))
    CONN.commit()
    print "Successfully added student: %s %s" %(first_name,last_name)

def make_new_project(title,description, max_grade):
    description=" ".join(description)
    query = """INSERT into Projects values (?,?,?)"""
    DB.execute(query, (title, description,max_grade))
    CONN.commit()
    print "Successfully added Project: %s" %(title)

def give_a_grade(first_name,last_name,project,grade):
    query = """SELECT github FROM Students WHERE first_name = ? and last_name = ?"""
    DB.execute(query, (first_name,last_name))
    fetched_github = DB.fetchone()
    query2 = """INSERT INTO Grades VALUES (?,?,?)"""
    DB.execute(query2, (fetched_github[0],project,grade))
    CONN.commit()
    print "Successfully added grade of %s for %s %s on their %s project" %(grade,first_name,last_name,project)


def connect_to_db():
    global DB, CONN
    CONN = sqlite3.connect("hackbright.db")
    DB = CONN.cursor()

def main():
    connect_to_db()
    command = None

    while command != "quit":
        input_string = raw_input("'h' for help, 'quit' to quit> ")
        tokens = input_string.split()
        command = tokens[0]
        args = tokens[1:]

        if command == "student":
            if len(args)==1:
                get_student_by_github(*args) 
            else: 
                print "You need to give us a github handle"
        elif command == "new_student":
            if len(args)==3:
                make_new_student(*args)
            else:
                print "You need to give us a first name, last name and github handle."
        elif command == "projects":
            if len(args) == 1:            
                get_projects_by_title(*args) #projects Markov ... then print max grade and description
            else:
                print "Simply print projects+title"
        elif command == "project_grade":
            if len(args) == 3:
                get_grade_by_student_project(*args)  #returns student's grade give a project
            else:
                print "We need first name, last name and project title to complete that query"
        elif command == "new_grade":
            if get_projects_by_title(tokens[3]):
                give_a_grade(*args) #"new_grade firstname lastname project grade"... then print a notice.
        elif command == "new_project":
            if len(args) < 3:
                print "You need to give us a project, description and max score."
            else:
                descrip = tokens[2:-1]
                make_new_project(args[0],descrip,args[-1])
        elif command == "report_card":
            if len(args) == 2:
                grades_by_student(*args)
            else:
                print "You need to give us first name and last name of student."

        elif command == "h":
            print """\n------------------------------------------------
            \nView student info by github handle: \n >> student <github> 
            \nView individual projects with description and max grades:\n >> projects <project title>
            \nView an individual's grade for a specific project.\n >> project_grade <first name> <last name> <project title>
            \nView an individual's report card. \n >> report_card <first name> <last name>
            \nAdd new student:\n >> new_student <first name> <last name> <github>
            \nAdd a new grade for a specific student and project.\n >> new_grade <first name> <last name> <project title> <grade>
            \nAdd a new project.\n >> new_project <description> <max score>
            \n---------------------------------------------------------
            """

            
    CONN.close()

if __name__ == "__main__":
    main()
