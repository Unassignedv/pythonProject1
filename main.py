import psycopg2
from flask import Flask, render_template, request, redirect

app = Flask(__name__)

conn = psycopg2.connect(database="service_db",
                        user="postgres",
                        password="23501690",
                        host="localhost",
                        port="5432")
cursor = conn.cursor()


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if len(username) == 0:
            return render_template('error.html', error="Username пуст")
        elif len(password) == 0:
            return render_template('error.html', error="Password пуст")
        cursor.execute("SELECT * FROM public.users WHERE login=%s AND password=%s", (str(username), str(password)))
        records = list(cursor.fetchall())  # [(1, 'Username', 'login', 'password'), (2, 'Username', 'login', 'password')]
        if len(records) == 0:
            return render_template('error.html', error="User not found")

        return render_template('account.html', full_name=records[0][1], login=records[0][2], password=records[0][3])
    return render_template("login.html")


@app.route('/registration', methods=['POST', 'GET'])
def registration():
    if request.method == 'POST':
        name = request.form.get('name')
        username = request.form.get('username')
        password = request.form.get('password')
        password_confirm = request.form.get('passwordConfirm')
        if len(username) == 0:
            return render_template('error.html', error="Username пуст")
        elif len(name) == 0:
            return render_template('error.html', error="Name пуст")
        elif len(password) == 0:
            return render_template('error.html', error="Password пуст")
        elif str(password_confirm) != str(password):
            return render_template('error.html', error="Пароли не равны друг другу")
        cursor.execute('INSERT INTO public.users (full_name, login, password) VALUES (%s, %s, %s);', (str(name), str(username), str(password)))
        conn.commit()
        return redirect('/login')
    return render_template('registration.html')


if __name__ == '__main__':
    app.run()
