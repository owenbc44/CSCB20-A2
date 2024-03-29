import sqlite3
from flask import Flask, render_template, request, g,session, redirect, url_for, escape, flash

DATABASE = 'assignment3.db'

# connects to the database
def get_db():
    # if there is a database, use it
    db = getattr(g, '_database', None)
    if db is None:
        # otherwise, create a database to use
        db = g._database = sqlite3.connect(DATABASE)
    return db

# converts the tuples from get_db() into dictionaries
# (don't worry if you don't understand this code)
def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

# given a query, executes and returns the result
# (don't worry if you don't understand this code)
def query_db(query, args=(), one=False):
    cur = get_db().execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

# tells Flask that "this" is the current running app
app = Flask(__name__)
app.secret_key=b'abbas'

# this function gets called when the Flask app shuts down
# tears down the database connection
@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        # close the database if we are connected to it
        db.close()

@app.route('/')
def index():
	if 'username' in session:
		user_id = session["username"]
		return render_template("index.html", user_id = user_id)
	return redirect(url_for('login'))

@app.route('/calendar')
def calendar():
	if 'username' in session:
		user_id = session["username"]
		return render_template("calendar.html", user_id = user_id)
	return redirect(url_for('login'))

@app.route('/lectures')
def lectures():
	if 'username' in session:
		user_id = session["username"]
		return render_template("lectures.html", user_id = user_id)
	return redirect(url_for('login'))

@app.route('/tutorials')
def tutorials():
	if 'username' in session:
		user_id = session["username"]
		return render_template("tutorials.html", user_id = user_id)
	return redirect(url_for('login'))

@app.route('/assignments')
def assignments():
	if 'username' in session:
		user_id = session["username"]
		return render_template("assignments.html", user_id = user_id)
	return redirect(url_for('login'))

@app.route('/tests')
def tests():
	if 'username' in session:
		user_id = session["username"]
		return render_template("tests.html", user_id = user_id)
	return redirect(url_for('login'))

@app.route('/links')
def links():
	if 'username' in session:
		user_id = session["username"]
		return render_template("links.html", user_id = user_id)
	return redirect(url_for('login'))

@app.route('/feedback')
def feedback():
	if 'username' in session:
		user_id = session["username"]
		# loading up different views based on student, instructor
		if session.get('instructor'):
			db = get_db()
			db.row_factory = make_dicts

			# retrieving all feedbacks for a specific instructor from sql, sending them to html
			feedbacks = query_db("SELECT question, comment FROM feedback WHERE username = ?",[session['username']], one=False)
			db.close()
			return render_template("feedback.html", feedbacks = feedbacks, user_id = user_id)
		elif session.get('student'):
			db = get_db()
			db.row_factory = make_dicts
			# retrieving all instructors available to provide feedback to
			instructors = query_db("SELECT username FROM instructors", one=False)
			return render_template("feedback.html",instructors = instructors, message=request.args.get('message'), user_id = user_id)
	return redirect(url_for('login'))

@app.route('/remark')
def remark():
	if 'username' in session:
		user_id = session["username"]

		# loading up different views based on student, instructor
		if session.get('instructor'):
			db = get_db()
			db.row_factory = make_dicts
			# retrieving all remark requests to view for instructor
			remarks = query_db("SELECT username, mark_id, comment, status FROM remark_requests", one=False)
			db.close()
			return render_template("remark.html", remarks = remarks, user_id = user_id)
		if session.get('student'):
			db = get_db()
			# retrieving status of a user's remark request
			requests = query_db("SELECT mark_id, status FROM remark_requests where username=?"
				, [session['username']], one=False)
			db.close()
			return render_template("remark.html", requests = requests, user_id = user_id)
	return redirect(url_for('login'))

@app.route('/markAsDone', methods=['GET','POST'])
def markAsDone():
	if 'username' in session:
		if request.method=="POST":
			mark_id=request.form.get('mark_id')
			db=get_db()
			db.row_factory = make_dicts
			query_db("update remark_requests set status = 'addressed' where username = ? and mark_id = ?"
				, [session.get('username'), mark_id])
			db.commit()
			db.close()
			return redirect(url_for('remark'))
		else:
			return redirect(url_for('remark'))
	return redirect(url_for('login'))

@app.route('/grades')
def retrieveGrades():
	if 'username' in session:
		user_id = session["username"]
		student_session = session.get('student')
		instructor_session = session.get('instructor')
		db = get_db()
		db.row_factory = make_dicts
		if student_session:
			# retrieving all grades for a specific user
			student_grades = query_db(
				"SELECT mark_id, mark FROM marks WHERE username = ?",[session['username']] , one=False)
			db.close()
			return render_template("grades.html", student_grades = student_grades, user_id = user_id)
		if instructor_session:

			# retrieving all marks for all students
			students = query_db("SELECT username FROM students", one=False)
			sql ="""select s.username,	sum(case when m.mark_id = 'Q1' then m.mark end) Q1
				,	sum(case when m.mark_id = 'Q2' then m.mark end) Q2
				,	sum(case when m.mark_id = 'Q3' then m.mark end) Q3
				,	sum(case when m.mark_id = 'Q4' then m.mark end) Q4
				,	sum(case when m.mark_id = 'A1' then m.mark end) A1
				,	sum(case when m.mark_id = 'A2' then m.mark end) A2
				,	sum(case when m.mark_id = 'A3' then m.mark end) A3
				,	sum(case when m.mark_id = 'Final' then m.mark end) Final
				from students s 
				left outer join marks m on m.username=s.username 
				group by s.username"""
			instructor_grades = query_db(sql, one=False)
			db.close()
			return render_template("grades.html", instructor_grades = instructor_grades, students = students, user_id = user_id)
	
	return redirect(url_for('login'))

@app.route('/enterGrades', methods=['GET','POST'])
def enterGrades():
	if 'username' in session:
		if request.method=='POST':
			# getting all values for POST request
			db = get_db()
			db.row_factory = make_dicts
			username = request.form.get('studentname')
			assessment = request.form.get('aName')
			mark = request.form.get('markvalue')

			# error check for empty, string and integer values
			if (username == 'Select an instructor') or (assessment == 'Select an assessment') or (mark == '') or (not mark.isdigit()):
				flash("*Please fill all the fields provided")
				return redirect("/grades")
			if not ( int(mark) >=0 and int(mark) <=100):
				flash("*Enter a mark between 0 - 100")
				return redirect("/grades")

			# checking if user with a given mark exists
			marks = query_db("SELECT username FROM marks where username = ? and mark_id = ?",[username, assessment])
			# if user doesn't have a mark, we do an INSERT INTO statement, whereas if a student does its UPDATE
			if marks:
				query_db("update marks set mark = ? where username = ? and mark_id = ?"
				,[mark, username, assessment])
			else:
				query_db("INSERT INTO marks (username, mark_id, mark) VALUES (?, ?, ?)", [
				username, assessment, mark])
			db.commit()
			db.close()
			flash("Your grades have been submitted successfully!")
			return redirect("/grades")
		else:
			return redirect("/grades")
	return redirect(url_for('login'))


@app.route('/remarkRequest', methods=['GET','POST'])
def remarkRequest():
	if 'username' in session:
		# getting all values for POST request
		student_session = session.get('student')
		instructor_session = session.get('instructor')
		username = session.get('username')
		assignment = request.form.get('aName')
		reason = request.form.get('reason')
		

		db = get_db()
		db.row_factory = make_dicts
		
		if request.method=='POST':
			# error check
			if (assignment == 'Select an evaluation') or (reason == ''):
				flash("*Please fill all the fields provided")
				return redirect(url_for("remark"))

			# inserting remark request into database
			query_db("INSERT INTO remark_requests (username, mark_id, comment, status) VALUES (?, ?, ?, 'in progress')", [
				username, assignment, reason])
			db.commit()
			db.close()
			message="Your remark request has been submitted!"
			flash("Your remark request has been submitted!")
			return redirect(url_for("remark", message=message))
	return redirect(url_for('login'))

@app.route('/sendFeedback', methods=['GET','POST'])
def sendFeedback():
	if 'username' in session:

		student_session = session.get('student')
		instructor_session = session.get('instructor')
		instructor = request.form.get('instructorname')
		feedback1 = request.form.get('feedback1')
		feedback2 = request.form.get('feedback2')
		feedback3 = request.form.get('feedback3')
		feedback4 = request.form.get('feedback4')

		db = get_db()
		db.row_factory = make_dicts
			# insert into db

		if request.method=='POST':
			# error check
			if (instructor == 'Select an instructor') or (feedback1 == '') or (feedback2 == '') or (feedback3 == '') or (feedback4 == '') :
				flash("*Please fill all the fields provided")
				return redirect(url_for('feedback'))

			# inserting feedback values into sql
			query_db("INSERT INTO feedback (username, question, comment) VALUES (?, ?, ?)", [
				instructor, 'What do you like about the instructor teaching?', feedback1])
			query_db("INSERT INTO feedback (username, question, comment) VALUES (?, ?, ?)", [
				instructor, 'What do you recommend the instructor to do to improve their teaching?', feedback2])	
			query_db("INSERT INTO feedback (username, question, comment) VALUES (?, ?, ?)", [
				instructor, 'What do you like about the labs?', feedback3])	
			query_db("INSERT INTO feedback (username, question, comment) VALUES (?, ?, ?)", [
				instructor, 'What do you recommend the lab instructors to do to improve their lab teaching?', feedback4])	

			db.commit()
			db.close()
			message="Your anonymous feedback has been submitted successfully!"
			flash("Your anonymous feedback has been submitted successfully!")
			return redirect(url_for("feedback", message=message))
	return redirect(url_for('login'))

@app.route('/register',methods=['GET','POST'])
def register():
	if 'username' in session:
		return redirect(url_for('index'))
	elif request.method=='POST':
		username=request.form.get('username')
		password=request.form.get('password')
		usertype=request.form.get('usertype')
		if usertype is not None:
			usertype+="s"
		lecsession=request.form.get('session')
		if len(username)<1:
			error="please enter a username"
			return render_template("register.html", error=error)
		elif len(password)<1:
			error="please enter a password"
			return render_template("register.html", error=error)
		elif usertype not in ("students", "instructors"):
			error="please pick a user type"
			return render_template("register.html", error=error)
		if usertype == "students":
			sql1 = "SELECT * FROM students"
		elif usertype == "instructors":
			sql1 = "SELECT * FROM instructors"
		
		db = get_db()
		results = query_db(sql1, args=(), one=False)
		for result in results:
			if result[0]==username:
				error="username "+username+" is already taken, please pick a different one"
				return render_template("register.html", error=error)
		if usertype == "students":
			sql2="insert into students values(?,?,?)"
			query_db(sql2, [username, password, lecsession])
			session['student'] = True
			session['instructor'] = False
		elif usertype == "instructors":
			sql2="insert into instructors values(?,?,?)"
			query_db(sql2, [username, password, lecsession])
			session['student'] = False
			session['instructor'] = True
		db.commit()
		db.close()
		session['username']=request.form['username']
		return redirect(url_for('index'))
	else:
		return render_template("register.html")

@app.route('/login',methods=['GET','POST'])
def login():
	error=None
	if request.method=='POST':
		db = get_db()
		sql = """
			SELECT *
			FROM students
			"""
		
		# For the student case
		session['student'] = True
		session['instructor'] = False

		results = query_db(sql, args=(), one=False)
		for result in results:
			if result[0]==request.form['username']:
				if result[1]==request.form['password']:
					session['username']=request.form['username']
					db.close()
					return redirect(url_for('index'))
		error="Incorrect username or password"
		return render_template('login.html', error=error)
	elif 'username' in session:
		return redirect(url_for('index'))
	else:
		return render_template("login.html")

@app.route('/instructorLogin',methods=['GET','POST'])
def instructorLogin():
	error=None
	if request.method=='POST':
		db = get_db()
		sql = """
			SELECT *
			FROM instructors
			"""
		
		# For the student case
		session['student'] = False
		session['instructor'] = True

		results = query_db(sql, args=(), one=False)
		for result in results:
			if result[0]==request.form['username']:
				if result[1]==request.form['password']:
					session['username']=request.form['username']
					db.close()
					return redirect(url_for('index'))
		error="Incorrect username or password"
		return render_template('instructorLogin.html', error=error)
	elif 'username' in session:
		return redirect(url_for('index'))
	else:
		return render_template("instructorLogin.html")

@app.route('/logout')
def logout():
	session.pop('username', None)
	session.pop('student', None)
	session.pop('instructor', None)
	return redirect(url_for('login'))

if __name__=="__main__":
	app.run(host='0.0.0.0')
