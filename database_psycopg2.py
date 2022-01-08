import psycopg2

hostname = 'localhost'
database = 'user_students'
username = 'postgres'
pwd = ''
port_id = 5432
conn = None
cur = None

try:
    conn = psycopg2.connect(
        host = hostname,
        dbname = database,
        user = username,
        password = pwd,
        port = port_id)

    cur = conn.cursor()

    cur.execute('DROP TABLE IF EXISTS employee')

    create_script = '''CREATE TABLE IF NOT EXISTS employee (
        id         int PRIMARY KEY,
        name       varchar(40) NOT NULL,
        salary     int,
        dept_id    varchar(30)) '''

    cur.execute(create_script)

    insert_script = "INSERT INTO employee (id, name, salary, dept_id) VALUES (%s, %s, %s, %s)"
    name = input('Input name: ')
    salary = int(input('Input salary: '))
    occupation = input('Input occupation: ')
    insert_values = [(1, name, salary, occupation)]

    for record in insert_values:
        cur.execute(insert_script, record)

    insert_script = "INSERT INTO employee (id, name, salary, dept_id) VALUES (%s, %s, %s, %s)"
    print('Now input the next one.')
    name = input('Input name: ')
    salary = int(input('Input salary: '))
    occupation = input('Input occupation: ')
    insert_values = [(2, name, salary, occupation)]

    for record in insert_values:
        cur.execute(insert_script, record)

    cur.execute('SELECT * FROM EMPLOYEE')
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
