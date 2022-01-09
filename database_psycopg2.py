import psycopg2
from tkinter import *

root = Tk()
root.title('database')
root.geometry("500x500")

hostname = 'localhost'
database = 'people_information'
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

        create_script = '''CREATE TABLE IF NOT EXISTS people_information (
            id         SERIAL PRIMARY KEY,
            name       varchar(40) NOT NULL,
            salary     int,
            occupation    varchar(30)) '''

        cur.execute(create_script)

        insert_script = "INSERT INTO people_information (name, salary, occupation) VALUES (%s, %s, %s)"

        insert_values = [(name_entry.get(), salary_entry.get(), occupation_entry.get())]

        for record in insert_values:
            cur.execute(insert_script, record)

        cur.execute('SELECT * FROM PEOPLE_INFORMATION')
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

    c.execute("SELECT * FROM people_information")
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

    c.execute("DELETE FROM user_students WHERE id = " + delete_box.get())

    delete_box.delete(0, END)

    conn.commit()

    conn.close()

delete_box = Entry(root, width=30)
delete_box.grid(row=9, column=1, pady=5)

delete_btn = Button(root, text="Delete record", command=delete)
delete_btn.grid(row=10, column =0, columnspan=2, pady=10, padx=10, ipadx=136)

name_entry = Entry(root, width = 30, font=('Arial 15'))
name_entry .grid(row=0, column =1, padx=20, pady=(10, 0))

salary_entry  = Entry(root, width = 30, font=('Arial 15'))
salary_entry .grid(row=1, column =1, padx=20)

occupation_entry  = Entry(root, width = 30, font=('Arial 15'))
occupation_entry .grid(row=2, column =1, padx=20)

#name, salary, and occupation labels:

name_label = Label(root, text= "Name:", font = ("Bahnschrift", 14))
name_label.grid(row=0, column = 0, pady=(10, 0))
salary_label = Label(root, text= "Salary:", font = ("Bahnschrift", 14))
salary_label.grid(row=1, column = 0)
occupation_label = Label(root, text= "Occupation:", font = ("Bahnschrift", 14))
occupation_label.grid(row=2, column = 0)

#submit button:

submit_button = Button(root, text="Add record to database", font=('Arial 15'), command=update)
submit_button.grid(row=6, column =0, columnspan=2, pady=10, padx=10, ipadx=137)

#query button
query_btn = Button(root, text="Show records", font=('Arial 15'), command=query)
query_btn.grid(row=16, column =0, columnspan=2, pady=10, padx=10, ipadx=134)

root.mainloop()
