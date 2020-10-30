from flask import Flask, render_template, request,url_for,redirect,session
import sqlite3
import os
import smtplib
app = Flask(__name__)

app.secret_key=os.urandom(30)

#GO TO INDEX PAGE
@app.route('/')
def a():
    return render_template('index.html')

#ADMIN LOGIN PAGE
@app.route('/adminlogin')
def b():
    return render_template('adminlogin.html')

# CHECK WHETHER IT IS ADMIN OR NOT
@app.route('/admin', methods=['POST', 'GET'])
def c():
    msg = "msg"
    if request.method=="POST":
        username = request.form["username"]
        password = request.form["password"]
        with sqlite3.connect("psglogin.db") as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
        find_user = ("SELECT * FROM admin WHERE username =? AND password = ?")
        cursor.execute(find_user, [(username), (password)])
        rows = cursor.fetchall()
        if rows:
            for i in rows:
                msg=i[0]
            session['adminname'] = msg
            return redirect(url_for('checking'))
        else:
            msg = "YOU CANNOT LOGIN"
            return render_template("fail.html", msg=msg)
@app.route('/checking')
def checking():
    adminname = session.get("adminname")
    return render_template('admin.html', adminname=adminname)

#FORM FOE ADDING HOD
@app.route('/addhod')
def d():
    return render_template("addhod.html")

#ADDING HOD TO DB
@app.route('/redirect',methods=['POST','GET'])
def e():
    msg = "msg"
    if request.method == "POST":
        try:
            name= request.form["name"]
            password = request.form["password"]
            username = request.form["username"]
            department=request.form["department"]
            qualification=request.form["qualification"]
            address=request.form["address"]
            attendance=request.form["attendance"]
            with sqlite3.connect("psglogin.db") as con:
                cur = con.cursor()
                cur.execute("INSERT into  addhod (name, password,username,department, qualification,address,attendance) values (?,?,?,?,?,?,?)", (name, password,username,department, qualification,address,attendance))
                con.commit()
        except:
            con.rollback()
            msg = "We can not add the HOD to the list"
            return render_template('fail.html',msg=msg)
        finally:
            return redirect(url_for('checking'))
            con.close()

#ADMIN LOGOUT
@app.route('/logoutadmin')
def logoutadmin():
    session.pop('adminname',None)
    return render_template('index.html')

#VIEW HOD FROM DB
@app.route("/viewhod")
def hodview():
    con = sqlite3.connect('psglogin.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute('select id, NAME, DEPARTMENT, QUALIFICATION, ADDRESS from addhod')
    rows = cur.fetchall()
    return render_template("viewhod.html", rows = rows)

#VIEW HOD ATTENDANCE
@app.route("/viewhodattendance")
def q():
    con = sqlite3.connect('psglogin.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute('select id, NAME, DEPARTMENT, ATTENDANCE from addhod')
    rows = cur.fetchall()
    return render_template("viewhodattendance.html", rows=rows)

#MARK HOD ATTENDANCE
@app.route('/markhodattendance',methods=['POST','GET'])
def markhod():
    msg = "msg"
    if request.method == "POST":
        try:
            id= request.form["id"]
            attendance = request.form["attendance"]
            with sqlite3.connect("psglogin.db") as con:
                cur = con.cursor()
                cur.execute("update addhod set attendance=? where id=?", (attendance,id))
                con.commit()
        except:
            con.rollback()
            msg = "The attendance cannnot be marked"
            return render_template('fail.html',msg=msg)
        finally:
            return redirect(url_for('hodattend'))
            con.close()

@app.route('/markinghodattendance')
def hodattend():
    con = sqlite3.connect('psglogin.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute('select * from addhod')
    rows = cur.fetchall()
    return render_template("markhodattendance.html", rows=rows)

@app.route("/hod")
def g():
    return render_template("hod.html")

#LOGIN PAGE FOR HOD
@app.route('/checkhod',methods=['POST','GET'])
def h():
    msg = "msg"
    while True:
        username = request.form["username"]
        password = request.form["password"]
        with sqlite3.connect("psglogin.db") as db:
            cursor = db.cursor()
        find_user = ("SELECT * FROM addhod WHERE username =? AND password = ?")
        cursor.execute(find_user, [(username), (password)])
        results = cursor.fetchall()
        if results:
            for i in results:
                msg=i[4]
            session['dept']=msg
            return redirect(url_for('check'))

        else:
            msg = "YOU CANNOT LOGIN"
            return render_template("fail.html", msg=msg)

@app.route('/check')
def check():
    dept = session.get("dept")
    return render_template('confirmhod.html',dept=dept)

#ADDING TUTOR TO DB
@app.route("/addtutor")
def i():
    return render_template("addtutor.html")

@app.route('/tutor',methods=['POST','GET'])
def j():
    msg = "msg"
    if request.method == "POST":
        try:
            name=request.form["name"]
            username= request.form["username"]
            password = request.form["password"]
            dept=session.get("dept")
            qualification=request.form["qualification"]
            address = request.form["address"]
            attendance = request.form["attendance"]
            with sqlite3.connect("psglogin.db") as con:
                cur = con.cursor()
                cur.execute("INSERT into  addtutor (name, password,username,department, qualification,address,attendance) values (?,?,?,?,?,?,?)", (name, password,username,dept, qualification,address,attendance))
                con.commit()
        except:
            con.rollback()
            msg = "We can not add the TUTOR to the list"
            return render_template("fail.html")
        finally:
            return redirect(url_for('check'))
            con.close()

# view tutor
@app.route('/viewtutor')
def tutview():
    con = sqlite3.connect('psglogin.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    dept = session.get("dept")
    cur.execute('select id, NAME,?, QUALIFICATION, ADDRESS from addtutor where DEPARTMENT = ?', (dept, dept))
    rows = cur.fetchall()
    return render_template("viewtutor.html", rows=rows,dept=dept)

#MARK TUTOR ATTENDANCE
@app.route('/marktutorattendance',methods=['POST','GET'])
def ss():
    msg = "msg"
    if request.method == "POST":
        try:
            id= request.form["id"]
            attendance = request.form["attendance"]
            with sqlite3.connect("psglogin.db") as con:
                cur = con.cursor()
                cur.execute("update addtutor set attendance=? where id=?", (attendance,id))
                con.commit()
        except:
            con.rollback()
            msg = "you cannot mark tutor attendance"
            return render_template('fail.html',msg=msg)
        finally:
            return redirect(url_for('tutorattend'))
            con.close()

@app.route('/markingtutorattendance')
def tutorattend():
    con = sqlite3.connect('psglogin.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    dept=session.get('dept')
    cur.execute('select id,?,attendance,name from addtutor where department=?',(dept,dept))
    rows = cur.fetchall()
    return render_template("marktutorattendance.html", rows=rows,dept=dept)

#VIEW TUTOR ATTENDANCE
@app.route('/viewtutorattendance')
def viewtutorattend():
    con = sqlite3.connect('psglogin.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    dept = session.get('dept')
    cur.execute('select id,name,attendance,? from addtutor where department=?', (dept, dept))
    rows = cur.fetchall()
    return render_template("viewtutorattendance.html", rows=rows,dept=dept)

#HOD PROFILE
@app.route('/hodprofile')
def hodprofile():
    con = sqlite3.connect('psglogin.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    dept = session.get('dept')
    cur.execute('select id,?,name,qualification,attendance from addhod where department=?', (dept,dept))
    rows = cur.fetchall()
    return render_template("viewhodprofile.html", rows=rows,dept=dept)

#HOD LOGOUT
@app.route('/logouthod')
def logo():
    session.pop('dept',None)
    return render_template('index.html')

#TUTOR LOGIN
@app.route('/tutorlogin')
def x():
    return render_template('tutor.html')

@app.route('/checktutor', methods=['POST', 'GET'])
def unibic():
        msg = "msg"
        while True:
            username = request.form["username"]
            password = request.form["password"]
            with sqlite3.connect("psglogin.db") as db:
                cursor = db.cursor()
            find_user = ("SELECT * FROM addtutor WHERE username =? AND password = ?")
            cursor.execute(find_user, [(username), (password)])
            results = cursor.fetchall()
            if results:
                for i in results:
                    msg = i[4]
                session['dept'] = msg
                return redirect(url_for('tutorcheck'))

            else:
                msg = "YOU CANNOT LOGIN"
                return render_template("fail.html", msg=msg)

@app.route('/tutorcheck')
def tutorcheck():
    dept = session.get("dept")
    return render_template('confirmtutor.html', dept=dept)

#ADDING STAFF
@app.route("/addstaff")
def milkbikkie():
    return render_template("addstaff.html")

@app.route('/staff',methods=['POST','GET'])
def tiger():
    msg = "msg"
    if request.method == "POST":
        try:
            id=request.form["id"]
            sub=request.form["sub"]
            dept=session.get("dept")
            with sqlite3.connect("psglogin.db") as con:
                cur = con.cursor()
                cur.execute("INSERT into  addstaff (id,department,subject) values (?,?,?)", (id,dept,sub))
                con.commit()
        except:
            con.rollback()
            msg = "We can not Add staff"
            return render_template("fail.html")
        finally:
            return redirect(url_for('tutorcheck'))
            con.close()

#VIEW STAFF
@app.route('/viewstaff')
def staffview():
    con = sqlite3.connect('psglogin.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    dept = session.get("dept")
    cur.execute('select * from staffs where id IN (select id from addstaff where department=?)',(dept,))
    rows = cur.fetchall()
    return render_template("viewstaff.html", rows=rows,dept=dept)

#ADD STUDENT
@app.route("/addstudent")
def student_html():
    return render_template("addstudent.html")

@app.route('/student',methods=['POST','GET'])
def student_post():
    msg = "msg"
    if request.method == "POST":
        try:
            id=request.form["id"]
            name= request.form["name"]
            username = request.form["username"]
            password= request.form["password"]
            dob = request.form["dob"]
            department=session.get("dept")
            with sqlite3.connect("psglogin.db") as con:
                cur = con.cursor()
                cur.execute("INSERT into  student (id,name,username,password,department,dob) values (?,?,?,?,?,?)", (id,name,username,password,department,dob))
                con.commit()
        except:
            con.rollback()
            msg = "We can not add student to the list"
            return render_template("fail.html")
        finally:
            return render_template('addstudentmark.html',id=id)

#STUDENT MARK
@app.route('/addstudentmark',methods=['POST','GET'])
def student_mark():
    msg = "msg"
    if request.method == "POST":
        try:
            id=request.form["id"]
            sub1= request.form["sub1"]
            sub2 = request.form["sub2"]
            sub3= request.form["sub3"]
            sub4 = request.form["sub4"]
            department=session.get("dept")
            with sqlite3.connect("psglogin.db") as con:
                cur = con.cursor()
                cur.execute("INSERT into  studentmark (id,subject) values (?,?)", (id,sub1))
                con.commit()
                cur.execute("INSERT into  studentmark (id,subject) values (?,?)", (id, sub2))
                con.commit()
                cur.execute("INSERT into  studentmark (id,subject) values (?,?)", (id, sub3))
                con.commit()
                cur.execute("INSERT into  studentmark (id,subject) values (?,?)", (id, sub4))
                con.commit()
        except:
            con.rollback()
            msg = "We can not add the suject to the student"
            return render_template("fail.html")
        finally:
            return redirect(url_for('tutorcheck'))

#TUTOR LOGOUT
@app.route('/logouttutor')
def logouttutor():
    session.pop('dept',None)
    return render_template('index.html')

#STAFF LOGIN
@app.route("/stafflogin")
def staff_log():
    return render_template("stafflogin.html")

@app.route('/restaff', methods=['POST', 'GET'])
def mmtravels():
    msg = "msg"
    if request.method=="POST":
        username = request.form["username"]
        password = request.form["password"]
        with sqlite3.connect("psglogin.db") as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
        find_user = ("SELECT * FROM staffs WHERE username =? AND password = ?")
        cursor.execute(find_user, [(username), (password)])
        rows = cursor.fetchall()

        if rows:
            for i in rows:
                msg=i[0]
            session['name'] = msg
            return redirect(url_for('checkingstaff'))
        else:
            msg = "YOU CANNOT LOGIN"
            return render_template("fail.html", msg=msg)

@app.route('/checkingstaff')
def checkingstaff():
    name = session.get('name')
    return render_template('welcome.html', name=name)

@app.route('/checkingg')
def checkingg():
    name = session.get("name")
    return render_template('welcome.html',name=name)

#VIEW CLASS FOR THE STAFF
@app.route('/viewclass')
def viewclass():
    con = sqlite3.connect('psglogin.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    name = session.get("name")
    cur.execute('select * from addstaff where id IN (select id from addstaff where id=?)', (name,))
    rows = cur.fetchall()
    return render_template("viewclass.html", rows=rows,name=name)

#STAFF LOGOUT
@app.route('/logoutstaff')
def logoutstaff():
    session.pop('name', None)
    return render_template('index.html')

#UPDATE STUDENT MARK
@app.route('/showstumark',methods=['POST','GET'])
def showstumark():
    msg = "msg"
    if request.method == "POST":
        session["department"]=request.form["department"]
        session["subject"]=request.form["subject"]
        return redirect(url_for('smark'))

@app.route('/updatemark',methods=['POST','GET'])
def updatemark():
    msg = "msg"
    if request.method == "POST":
        try:
            id= request.form["id"]
            subject=request.form["subject"]
            mark= request.form["mark"]
            with sqlite3.connect("psglogin.db") as con:
                cur = con.cursor()
                cur.execute("update studentmark set mark=? where id=? and subject=?", (mark,id,subject))
                con.commit()
        except:
            con.rollback()
            msg = "We can not add the Mark to the list"
            return render_template('fail.html',msg=msg)
        finally:
            return redirect(url_for('smark'))
            con.close()

@app.route('/smark')
def smark():
    department= session.get('department')
    subject=session.get('subject')
    con = sqlite3.connect('psglogin.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    cur.execute('select * from studentmark where id in (select id from student where department=?) and subject=?',(department, subject))
    rows = cur.fetchall()
    return render_template('abcd.html', rows=rows)

#STUDENT LOGIN
@app.route("/studentlogin")
def student_log():
    return render_template("studentlogin.html")

@app.route('/checkstudent', methods=['POST', 'GET'])
def checkstu():
    msg = "msg"
    if request.method=="POST":
        username = request.form["username"]
        password = request.form["password"]
        with sqlite3.connect("psglogin.db") as db:
            db.row_factory = sqlite3.Row
            cursor = db.cursor()
        find_user = ("SELECT * FROM student WHERE username =? AND password = ?")
        cursor.execute(find_user, [(username), (password)])
        rows = cursor.fetchall()
        if rows:
            for i in rows:
                msg=i[0]
            session['name'] = msg
            return redirect(url_for('checkingstudent'))
        else:
            msg = "YOU CANNOT LOGIN"
            return render_template("fail.html", msg=msg)

@app.route('/checkingstudent')
def checkingstudent():
    name = session.get('name')
    return render_template('welcomestudent.html', name=name)

#VIEW MARK BY THE STUDENT
@app.route('/viewmark')
def viewmark():
    con = sqlite3.connect('psglogin.db')
    con.row_factory = sqlite3.Row
    cur = con.cursor()
    name = session.get("name")
    cur.execute('select * from  studentmark where id=?', (name,))
    rows = cur.fetchall()
    return render_template("viewmark.html", rows=rows,name=name)

@app.route('/logoutstudent')
def logoutstudent():
    session.pop('name', None)
    return render_template('index.html')

@app.route('/contact',methods=['POST','GET'])
def contact():
    msg = "msg"
    if request.method == "POST":
        try:
            name=request.form["name"]
            email= request.form["email"]
            subject = request.form["subject"]
            message=request.form["message"]
            server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            server.login("xxx@gmail.com", "password")
            dd =name+" "+email+" "+" "+message
            head='Subject :{}'.format(subject)
            aa=head+"\n\n"+dd
            server.sendmail("xxx@gmail.com","xxx.com", aa)
            server.quit()
            server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
            server.login("xxx@gmail.com", "password")
            sub="Response"
            hea = 'Subject :{}'.format(sub)
            con="YOUR RESPONSE HAVE BEEN DELIVERED"
            ss=hea+"\n\n"+con
            server.sendmail("xxx@gmail.com",email,ss)
            server.quit()
            return render_template("index.html")
        except:
            msg = "cannot send mail"
            return render_template("fail.html")
        finally:
            return render_template("index.html")

if __name__ == '__main__':
    app.run(debug=True)
