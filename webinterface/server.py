from flask import Flask, flash, render_template, redirect, url_for, request, session, escape
from module.database import Database
import MySQLdb

app = Flask(__name__)
app.secret_key = "mys3cr3tk3y"
db = Database()

db1 = MySQLdb.connect(host="localhost", user="cryptouser", passwd="123456", db="cryptodb")
cur = db1.cursor()


class ServerError(Exception):pass

@app.route('/')
def index():
    if 'username' in session:
        username_session = escape(session['username']).capitalize()
        return render_template('index.html', session_user_name=username_session)
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if 'username' in session:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username_form  = request.form['username']
        password_form  = request.form['password']
        cur.execute("SELECT COUNT(1) FROM users WHERE username = %s;", [username_form]) # CHECKS IF USERNAME EXSIST
        if cur.fetchone()[0]:
            cur.execute("SELECT password FROM users WHERE username = %s;", [username_form]) # FETCH THE HASHED PASSWORD
            for row in cur.fetchall():
                if password_form == row[0]:
                    session['username'] = request.form['username']
                    return redirect(url_for('index'))
                else:
                    error = "Invalid Credential"
        else:
            error = "Invalid Credential"
    return render_template('login.html', error=error)


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route('/add/')
def add():
    if 'username' in session:
        username_session = escape(session['username']).capitalize()
        return render_template('add.html', session_user_name=username_session)
    return redirect(url_for('login'))


@app.route('/adduser', methods = ['POST', 'GET'])
def adduser():
        if request.method == 'POST' and request.form['save']:
            if db.insert(request.form):
                flash("A new user has been added")
            else:
                flash("A new user can not be added")

            return redirect(url_for('users'))
        else:
            return redirect(url_for('users'))






#    if 'username' in session:
#        username_session = escape(session['username']).capitalize()
#        #return render_template('index.html', session_user_name=username_session)
#        if request.method == 'POST' and request.form['save']:
#            if db.insert(request.form):
#                flash("A new user has been added")
#            else:
#                flash("A new user can not be added")

#            return redirect(url_for('users'))
#        else:
#            return redirect(url_for('users'))

#    return redirect(url_for('login'))






@app.route('/delete/<int:id>/')
def delete(id):
    data = db.read(id)
    if 'username' in session:
        username_session = escape(session['username']).capitalize()
        if len(data) == 0:
            return redirect(url_for('users'))
        else:
            session['delete'] = id
        return render_template('delete.html', data = data, session_user_name=username_session)

    return redirect(url_for('login'))




@app.route('/deleteuser', methods = ['POST'])
def deleteuser():
    if request.method == 'POST' and request.form['delete']:

        if db.delete(session['delete']):
            flash('A user has been deleted')

        else:
            flash('A user can not be deleted')

        session.pop('delete', None)

        return redirect(url_for('users'))
    else:
        return redirect(url_for('users'))


####
@app.route('/users')
def users():
    data = db.read(None)
    if 'username' in session:
        username_session = escape(session['username']).capitalize()
        return render_template('/index_u.html', session_user_name=username_session, data = data)
    return redirect(url_for('login'))


@app.route('/update/<int:id>/')
def update(id):
    data = db.read(id)
    if 'username' in session:
        username_session = escape(session['username']).capitalize()

        if len(data) == 0:
            return redirect(url_for('users'))
        else:
            session['update'] = id
        return render_template('update.html', data = data, session_user_name=username_session)

    return redirect(url_for('login'))


@app.route('/updateuser', methods=['POST'])
def updateuser():
    if request.method == 'POST' and request.form['update']:

        if db.update(session['update'], request.form):
            flash('A user has been updated')

        else:
            flash('A user can not be updated')

        session.pop('update', None)

        return redirect(url_for('users'))
    else:
        return redirect(url_for('users'))

####
@app.route('/settings')
def settings():
    data = db.read_settings(None)

    if 'username' in session:
        username_session = escape(session['username']).capitalize()
        return render_template('/index_s.html', session_user_name=username_session, data = data)
    return redirect(url_for('login'))


@app.route('/updates/<int:id>/')
def updates(id):
    data = db.read_settings(id)

    if len(data) == 0:
        return redirect(url_for('settings'))
    else:
        session['update'] = id
        return render_template('update_s.html', data=data)


@app.route('/updatesettings', methods=['POST'])
def updatesettings():
    if request.method == 'POST' and request.form['update']:

        if db.update_settings(session['update'], request.form):
            flash('A settings has been updated')

        else:
            flash('A settings can not be updated')

        session.pop('update', None)

        return redirect(url_for('settings'))
    else:
        return redirect(url_for('settings'))



@app.route('/orders')
def orders():
    data = db.read_orders(None)

    if 'username' in session:
        username_session = escape(session['username']).capitalize()
        return render_template('/index_o.html', session_user_name=username_session, data = data)
    return redirect(url_for('login'))


@app.route('/closedorders')
def closedorders():
    data = db.read_corders(None)

    if 'username' in session:
        username_session = escape(session['username']).capitalize()
        return render_template('/index_co.html', session_user_name=username_session, data = data)
    return redirect(url_for('login'))


@app.route('/logs')
def logs():
    data = db.read_logs(None)

    if 'username' in session:
        username_session = escape(session['username']).capitalize()
        return render_template('/logs.html', session_user_name=username_session, data = data)
    return redirect(url_for('login'))

####


@app.route('/markets')
def markets():
    data = db.read_markets(None)

    if 'username' in session:
        username_session = escape(session['username']).capitalize()
        return render_template('/index_market.html', session_user_name=username_session, data = data)
    return redirect(url_for('login'))


@app.route('/updatem/<int:id>/')
def updatem(id):
    data = db.read_markets(id)
    if 'username' in session:
        username_session = escape(session['username']).capitalize()
        if len(data) == 0:
            return redirect(url_for('markets'))
        else:
            session['update'] = id
        return render_template('update_market.html', data = data, session_user_name=username_session)

    return redirect(url_for('login'))

@app.route('/updatemarket', methods=['POST'])
def updatemarket():
    if request.method == 'POST' and request.form['update']:

        if db.update_market(session['update'], request.form):
            flash('A market has been updated')

        else:
            flash('A market can not be updated')

        session.pop('update', None)

        return redirect(url_for('markets'))
    else:
        return redirect(url_for('markets'))

@app.route('/deletem/<int:id>/')
def deletem(id):
        data = db.read_markets(id)
        if 'username' in session:
            username_session = escape(session['username']).capitalize()
            if len(data) == 0:
                return redirect(url_for('markets'))
            else:
                session['delete'] = id
            return render_template('delete_market.html', data=data, session_user_name=username_session)

        return redirect(url_for('login'))

@app.route('/deletemarket', methods=['POST'])
def deletemarket():
        if request.method == 'POST' and request.form['delete']:

            if db.delete_markets(session['delete']):
                flash('A market has been deleted')

            else:
                flash('A market can not be deleted')

            session.pop('delete', None)

            return redirect(url_for('markets'))
        else:
            return redirect(url_for('umarkets'))

@app.route('/addm/')
def addm():
    if 'username' in session:
        username_session = escape(session['username']).capitalize()
        return render_template('add_market.html', session_user_name=username_session)
    return redirect(url_for('login'))



@app.route('/addmarket', methods=['POST', 'GET'])
def addmarket():
            if request.method == 'POST' and request.form['save']:
                if db.insert_market(request.form):
                    flash("A new market has been added")
                else:
                    flash("A new market can not be added")

                return redirect(url_for('markets'))
            else:
                return redirect(url_for('markets'))





#####
@app.errorhandler(404)
def page_not_found(error):
    return render_template('error.html')


if __name__ == '__main__':
    app.run(debug = True, port=8181, host="0.0.0.0")
