import psycopg2
from tkinter import *

root = Tk()
root.title('database')
root.geometry("500x500")

hostname = 'localhost'
database = 'user_students'
username = 'postgres'
pwd = ''
port_id = 5432
conn = None
cur = None

def update():
    try:
        conn = psycopg2.connect(
            host = hostname,
            dbname = database,
            user = username,
            password = pwd,
            port = port_id)

        cur = conn.cursor()

        cur.execute('DROP TABLE IF EXISTS user_students')

        create_script = '''CREATE TABLE IF NOT EXISTS user_students (
            id         SERIAL PRIMARY KEY,
            name       varchar(40) NOT NULL,
            salary     int,
            occupation    varchar(30)) '''

        cur.execute(create_script)

        insert_script = "INSERT INTO user_students (name, salary, occupation) VALUES (%s, %s, %s)"

        insert_values = [(name_editor.get(), salary_editor.get(), occupation_editor.get())]

        for record in insert_values:
            cur.execute(insert_script, record)

        cur.execute('SELECT * FROM USER_STUDENTS')
        for record in cur.fetchall():
            print(record)

        conn.commit()
    except Exception as error:
        print(error)
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()

def query():
    conn = psycopg2.connect(
            host = hostname,
            dbname = database,
            user = username,
            password = pwd,
            port = port_id)

    c = conn.cursor()

    c.execute("SELECT * FROM user_students")
    records = c.fetchall()
    #print(records)

    #loop through results
    print_records = ''
    for record in records[0:6]:
        print_records += str(record) + "\n"

    query_label = Label(root, text=print_records)
    query_label.grid(row=12, column=0, columnspan=2)


    conn.commit()

    conn.close()

def delete():
    conn = psycopg2.connect(
            host = hostname,
            dbname = database,
            user = username,
            password = pwd,
            port = port_id)

    c = conn.cursor()

    c.execute("DELETE FROM user_students WHERE name = " + delete_box.get())

    delete_box.delete(0, END)

    conn.commit()

    conn.close()


name_editor = Entry(root, width = 30)
name_editor.grid(row=0, column =1, padx=20, pady=(10, 0))

salary_editor = Entry(root, width = 30)
salary_editor.grid(row=1, column =1, padx=20)

occupation_editor = Entry(root, width = 30)
occupation_editor.grid(row=2, column =1, padx=20)

name_label = Label(root, text= "Name:")
name_label.grid(row=0, column = 0, pady=(10, 0))
salary_label = Label(root, text= "Salary:")
salary_label.grid(row=1, column = 0)
occupation_label = Label(root, text= "Occupation:")
occupation_label.grid(row=2, column = 0)

delete_box = Entry(root, width=30)
delete_box.grid(row=9, column=1, pady=5)

delete_btn = Button(root, text="Delete record", command=delete)
delete_btn.grid(row=10, column =0, columnspan=2, pady=10, padx=10, ipadx=136)

submit_button = Button(root, text="Add record to database", command=update)
submit_button.grid(row=6, column =0, columnspan=2, pady=10, padx=10, ipadx=137)

#query button
query_btn = Button(root, text="Show records", command=query)
query_btn.grid(row=16, column =0, columnspan=2, pady=10, padx=10, ipadx=134)

root.mainloop()
