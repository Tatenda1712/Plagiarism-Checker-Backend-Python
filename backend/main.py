from app import app
from werkzeug.security import generate_password_hash, check_password_hash
from db import mysql
from flaskext.mysql import MySQL
from flask import Flask, request,session,jsonify
from flask_cors import CORS, cross_origin
from datetime import timedelta
import pymysql
import os
from werkzeug.utils import secure_filename
import studentSimilarity

mysql = MySQL()

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'plagiarismchecker'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

UPLOAD_FOLDER='D:\Online Plagiarism Checking System Backend\Storage'

app=Flask(__name__)
app.secret_key="tatenda musodza"
app.config['UPLOAD_FOLDER']=UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH']=16*1024*1024
app.config['PERMANENT_SESSION_LIFETIME']=timedelta(minutes=10)
app.config['CORS_HEADERS']='Content-Type'
cors=CORS(app, resources={
    r"/studentregistration":{
        "origins":"http://localhost:5000"
    },
    r"/studentlogin":{
        "origins":"http://localhost:5000"
    },
    r"/adminlogin":{
        "origins":"http://localhost:5000"
    },
    r"/students":{
        "origins":"http://localhost:5000"
    },
    r"/courses":{
        "origins":"http://localhost:5000"
    },
    r"/lecturers":{
        "origins":"http://localhost:5000"
    },
    r"/lecturerlogin":{
        "origins":"http://localhost:5000"
    },
    r"/addlecturer":{
        "origins":"http://localhost:5000"
    },
    r"/addcourse":{
        "origins":"http://localhost:5000"
    },
    r"/setassignment":{
        "origins":"http://localhost:5000"
    },
    r"setstudentassignments":{
        "origins":"http://localhost:5000"
    },
    r"/lecturercourse/<string:leccourse>":{
        "origins":"http://localhost:5000"
    },
    r"/submitted/<string:course>'":{
        "origins":"http://localhost:5000"
    }
})
CORS(app)



@app.route('/studentregistration', methods=['POST','GET'])
@cross_origin(origin='localhost',headers=['Content-Type','Authorisation'])
def studentRegister():
    global cursor, conn;
    try:
        _json = request.json
        _fullname = _json['fullname']
        _regno = _json['regnumberreg']
        _password = _json['regpassword']
        conn = mysql.connect()
        cursor = conn.cursor()
        sql = "SELECT * FROM students WHERE regnumber=%s"
        sql_where = (_regno,)
        cursor.execute(sql, sql_where)
        row=cursor.fetchone()
        if row:
            return jsonify({'message':'Regstration number already used'})
        else:
            # validate the received values
            if _fullname and _regno and _password and request.method == 'POST':
                _hashed_password = generate_password_hash(_password)
                # save edits
                sql = "INSERT INTO students(fullname,regnumber,password) VALUES(%s,%s,%s)"
                data = (_fullname, _regno, _hashed_password)
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.execute(sql, data)
                conn.commit()
                resp = jsonify({'message':'You have Successfully Registered','user':_fullname,'regno':_regno})
                resp.status_code = 200
                return resp
            else:
                 return not_found()
    except Exception as e:
            print(e)
    finally:
            cursor.close()
            conn.close()


@app.route('/studentlogin',methods=['POST'])
@cross_origin(origin='localhost',headers=['Content-Type','Authorisation'])
def studentLogin():
    conn=None;
    cursor=None;
    try:
        _json=request.json
        _regnumber=_json['regnumber']
        _password=_json['password']
        #validate the received values
        if _regnumber and _password:
            #check user exists
            conn=mysql.connect()
            cursor=conn.cursor()
            sql="SELECT * FROM students WHERE regnumber=%s"
            sql_where=(_regnumber,)
            cursor.execute(sql,sql_where)
            row=cursor.fetchone()
            if row:
                if check_password_hash(row[2],_password):
                    session['regnumber']=row[1]
                    regno=row[1]
                    user=row[0]
                    sql = "SELECT * FROM setAssignments"
                    cursor.execute(sql)
                    row = cursor.fetchone()
                    #cursor.close
                    #conn.close
                    return  jsonify({'message':'You are logged in successfully',"regno":regno,'username':user})
                else:
                    resp=jsonify({'message':'Invalid Password'})
                    resp.status_code=400
                    return resp
            else:
                resp=jsonify({'message':'Invalid Credentials'})
                resp.status_code=400
                return resp
    except Exception as e:
        print(e)
    finally:
        if cursor and conn:
            cursor.close()
            conn.close()

#login function
@app.route('/lecturerlogin',methods=['POST'])
@cross_origin(origin='localhost',headers=['Content-Type','Authorisation'])
def lectureLogin():
    conn=None;
    cursor=None;
    try:
        _json=request.json
        _lecturerName=_json['lecusername']
        _password=_json['lecpassword']
        #validate the received values
        if _lecturerName and _password:
            #check user exists
            conn=mysql.connect()
            cursor=conn.cursor()
            sql="SELECT * FROM lecturers WHERE lecturername=%s"
            sql_where=(_lecturerName,)
            cursor.execute(sql,sql_where)
            row=cursor.fetchone()
            if row:
                if check_password_hash(row[2],_password):
                    session['lecturerName']=row[1]
                    #cursor.close
                    #conn.close
                    lecname=row[1]
                    leccourse=row[3]
                    return  jsonify({'message':'You are logged in successfully','lecturername':lecname, 'lecturercourse':leccourse})
                else:
                    resp=jsonify({'message':'Invalid Password'})
                    resp.status_code=400
                    return resp
            else:
                resp=jsonify({'message':'Invalid Credentials'})
                resp.status_code=400
                return resp
    except Exception as e:
        print(e)
    finally:
        if cursor and conn:
            cursor.close()
            conn.close()



#login api Admin
@app.route('/adminlogin',methods=['POST'])
@cross_origin(origin='localhost',headers=['Content-Type','Authorisation'])
def adminLogin():
    conn=None;
    cursor=None;
    try:
        _json=request.json
        _username=_json['adminuser']
        _password=_json['adminpassword']
        #validate the received values
        if _username and _password:
            #check user exists
            conn=mysql.connect()
            cursor=conn.cursor()
            sql="SELECT * FROM admin WHERE username=%s"
            sql_where=(_username,)
            cursor.execute(sql,sql_where)
            row=cursor.fetchone()
            if row:
                if check_password_hash(row[1],_password):
                    session['username']=row[0]
                    #cursor.close
                    #conn.close
                    username=row[0]
                    return  jsonify({'message':'You are logged in successfully','user':username})
                else:
                    resp=jsonify({'message':'Invalid Password'})
                    resp.status_code=400
                    return resp
            else:
                resp=jsonify({'message':'Invalid Credentials'})
                resp.status_code=400
                return resp
    except Exception as e:
        print(e)
    finally:
        if cursor and conn:
            cursor.close()
            conn.close()

#list students
@app.route('/students', methods=['GET', 'POST'])
@cross_origin(origin='localhost',headers=['Content-Type','Authorisation'])
def students():
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT fullname fullname, regnumber regnumber FROM students")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

      # add api
#adding lecturer
@app.route('/addlecturer', methods=['POST'])
@cross_origin(origin='localhost',headers=['Content-Type','Authorisation'])
def addLecturer():
    conn = None
    cursor = None
    try:
        _json = request.json
        _name = _json['lecturername']
        _course = _json['leccoursecode']
        _password = _json['lecpassword']
        conn = mysql.connect()
        cursor = conn.cursor()
        sql = "SELECT * FROM lecturers WHERE lecturername=%s"
        sql_where = (_name,)
        cursor.execute(sql, sql_where)
        row = cursor.fetchone()
        if row:
            return jsonify({'message': 'Lecturer Already Registered'})
        else:
            # validate the received values
            if _name and _course and _password and request.method == 'POST':
                _hashed_password = generate_password_hash(_password)
                # save edits
                sql = "INSERT INTO lecturers(lecturername,password,coursecode) VALUES(%s,%s,%s)"
                data = (_name, _hashed_password , _course)
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.execute(sql, data)
                conn.commit()
                resp = jsonify({'message':'Lecturer added Successfully'})
                resp.status_code = 200
                return resp
            else:
                 return not_found()
    except Exception as e:
            print(e)
    finally:
            cursor.close()
            conn.close()

#adding course
@app.route('/addcourse', methods=['POST'])
@cross_origin(origin='localhost',headers=['Content-Type','Authorisation'])
def addCourse():
    conn = None
    cursor = None
    try:
        _json = request.json
        _coursecode = _json['coursecode']
        _coursename = _json['coursename']
        conn = mysql.connect()
        cursor = conn.cursor()
        sql = "SELECT * FROM courses WHERE coursecode=%s"
        sql_where = (_coursecode,)
        cursor.execute(sql, sql_where)
        row = cursor.fetchone()
        if row:
            return jsonify({'message': 'Course already Registered'})
        else:
            # validate the received values
            if _coursename and _coursecode and request.method == 'POST':
                # save edits
                sql = "INSERT INTO courses(coursecode,coursename) VALUES(%s,%s)"
                data = (_coursecode, _coursename)
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.execute(sql, data)
                conn.commit()
                resp = jsonify({'message':'Course added Successfully'})
                resp.status_code = 200
                return resp
            else:
                 return not_found()
    except Exception as e:
            print(e)
    finally:
            cursor.close()
            conn.close()

#set assignments
@app.route('/setassignment', methods=['POST'])
@cross_origin(origin='localhost',headers=['Content-Type','Authorisation'])
def setAssignment():
    conn = None
    cursor = None
    try:
        _json = request.json
        _assignmentname = _json['setassignmentname']
        _course=_json['setcoursecode']
        _duedate = _json['setduedate']
        _lecturername = _json['setlecturername']
        # validate the received values
        if _assignmentname and _course and _duedate and request.method == 'POST':
            sql = "INSERT INTO setassignments(course,assignmentname,duedate, lecturername) VALUES(%s,%s,%s,%s)"
            data = (_course, _assignmentname, _duedate,_lecturername)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify({'message':'Assignment added Successfully'})
            resp.status_code = 200
            return resp
        else:
             return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


#list lecturers
@app.route('/lecturers', methods=['GET'])
@cross_origin(origin='localhost',headers=['Content-Type','Authorisation'])
def lecturers():
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id id, lecturername lecturername, coursecode coursecode FROM lecturers")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/courses', methods=['GET'])
@cross_origin(origin='localhost',headers=['Content-Type','Authorisation'])
def courses():
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id id, coursecode coursecode, coursename coursename FROM courses")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


#list asssignments
@app.route('/setassignmentslist', methods=['GET'])
@cross_origin(origin='localhost',headers=['Content-Type','Authorisation'])
def assignments():
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id id,course course, assignmentname assignmentname, duedate duedate FROM setassignments")
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


#list asssignments
@app.route('/setstudentassignments/<string:coursecode>', methods=['GET'])
@cross_origin(origin='localhost',headers=['Content-Type','Authorisation'])
def courseassignments(coursecode):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id id,course course, assignmentname assignmentname, duedate duedate, lecturername lecturername FROM setassignments  WHERE course=%s",coursecode)
        rows=cursor.fetchall()
        if rows:
            resp = jsonify(rows)
            resp.status_code = 200
            return resp
        else:
            return jsonify(({'message':'No Course Assignments Found'}))
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

#list asssignments
@app.route('/submitassignment/<int:id>', methods=['GET'])
@cross_origin(origin='localhost',headers=['Content-Type','Authorisation'])
def submitAssignments(id):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id id,course course, assignmentname assignmentname, duedate duedate, lecturername lecturername FROM setassignments  WHERE id=%s",id)
        row=cursor.fetchone()
        if row:
            resp = jsonify(row)
            resp.status_code = 200
            return resp
        else:
            return jsonify(({'message':'No Course Assignments Found'}))
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


#list asssignments
@app.route('/lecturercourse/<string:leccourse>', methods=['GET'])
@cross_origin(origin='localhost',headers=['Content-Type','Authorisation'])
def leccourseassignments(leccourse):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id id,course course, assignmentname assignmentname, duedate duedate, lecturername lecturername FROM setassignments  WHERE course=%s",leccourse)
        rows=cursor.fetchall()
        if rows:
            resp = jsonify(rows)
            resp.status_code = 200
            return resp
        else:
            return jsonify(({'message':'No Course Assignments Found'}))
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


#delete api

@app.route('/deletelecturer/<int:id>', methods=['DELETE','GET','POST'])
@cross_origin(origin='localhost',headers=['Content-Type','Authorisation'])
def deleteLecturer(id):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM lecturers WHERE id=%s", (id,))
        conn.commit()
        resp = jsonify('Lecturer Deleted Successfully!!!')
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/deletecourse/<int:id>', methods=['DELETE','GET','POST'])
@cross_origin(origin='localhost',headers=['Content-Type','Authorisation'])
def deleteCourse(id):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM courses WHERE id=%s", (id,))
        conn.commit()
        resp = jsonify('Course Deleted Successfully!!!')
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/deleteassignment/<int:id>', methods=['DELETE','GET','POST'])
@cross_origin(origin='localhost',headers=['Content-Type','Authorisation'])
def deleteLecAssignment(id):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM setassignments WHERE id=%s", (id,))
        conn.commit()
        resp = jsonify('Assignment Deleted Successfully!!!')
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()


@app.route('/deletestudent/<string:regno>', methods=['DELETE','GET','POST'])
@cross_origin(origin='localhost',headers=['Content-Type','Authorisation'])
def deleteStudent(regno):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE regnumber=%s", (regno,))
        conn.commit()
        resp = jsonify('Student Deleted Successfully!!!')
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/lecturerassignments/<string:lecturername>', methods=['GET'])
@cross_origin(origin='localhost',headers=['Content-Type','Authorisation'])
def AssignmentsSet(lecturername):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT id id, course course, assignmentname assignmentname, duedate duedate FROM setassignments WHERE lecturername=%s", lecturername)
        row = cursor.fetchall()
        conn.commit()
        resp = jsonify(row)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/submitted/<string:course>', methods=['GET'])
@cross_origin(origin='localhost',headers=['Content-Type','Authorisation'])
def submittedAssignments(course):
    conn = None
    cursor = None
    try:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT coursecode coursecode, assignmentname assignmentname, updated_at updated_at, regnumber regnumber, url url FROM assignments WHERE coursecode=%s", course)
        row = cursor.fetchall()
        conn.commit()
        resp = jsonify(row)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

#update api

#update lecturer
@app.route('/updatelecturer', methods=['PUT'])
@cross_origin(origin='localhost',headers=['Content-Type','Authorisation'])
def updateLecturer():
    conn = None
    cursor = None
    try:
        _json = request.json
        _id = _json['   id']
        _name = _json['name']
        _course = _json['course']
        _password = _json['pwd']
        # validate the received values
        if _name and _course and _password and _id and request.method == 'PUT':
            # do not save password as plain text
            _hashed_password = generate_password_hash(_password)
            # save edits
            sql = "UPDATE lecturers SET lecturerName=%s, password=%s, course=%s WHERE id=%s"
            data = (_name, _hashed_password, _course, _id,)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify('Lecturer Updated Successfully')
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
           print(e)
    finally:
        cursor.close()
        conn.close()

#update student
@app.route('/studentupdate/<string:regno>', methods=['PUT'])
@cross_origin(origin='localhost',headers=['Content-Type','Authorisation'])
def updateStudent(regno):
    conn = None
    cursor = None
    try:
        _json = request.json
        _fullname = _json['fullname']
        _regnumber = _json['regnumberreg']
        _password = _json['regpassword']
        # validate the received values
        if _fullname and _regnumber and _password and request.method == 'PUT':
            # do not save password as plain text
            _hashed_password = generate_password_hash(_password)
            # save edits
            sql = "UPDATE students SET fullname=%s, regnumber=%s, password=%s WHERE regnumber=%s"
            data = (_fullname,_regnumber, _hashed_password,)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify('Student Updated Successfully')
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
           print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/updateassignment', methods=['PUT'])
@cross_origin(origin='localhost',headers=['Content-Type','Authorisation'])
def updateAssignment():
    conn = None
    cursor = None
    try:
        _json = request.json
        _id = _json['id']
        _assginmentname = _json['assignmentname']
        _url = _json['url']
        _course = _json['course']
        # validate the received values
        if _assginmentname and _course and _url and _id and request.method == 'PUT':
            # save edits
            sql = "UPDATE assignments SET assignmentName=%s, url=%s, course=%s WHERE id=%s"
            data = (_assginmentname, _url, _course, _id,)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify('Asssignment Updated Successfully')
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
           print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/updatecourse',methods=['PUT'])
@cross_origin(origin='localhost',headers=['Content-Type','Authorisation'])
def updateCourse():
    conn = None
    cursor = None
    try:
        _json = request.json
        _id = _json['id']
        _coursecode = _json['coursecode']
        _courseName = _json['coursename']
        # validate the received values
        if _coursecode and _courseName and _id and request.method == 'PUT':
            # save edits
            sql = "UPDATE courses SET courseCode=%s, courseName=%s WHERE id=%s"
            data = (_coursecode, _courseName, _id,)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify('Course Updated Successfully')
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
           print(e)
    finally:
        cursor.close()
        conn.close()



# file upload api

ALLOWED_EXTENSIONS=set(['pdf'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploadassignment', methods=['POST','GET'])
@cross_origin(origin='localhost',headers=['Content-Type','Authorisation'])
def uploadAssignment():
    conn = None
    cursor = None
    data = request.get_data('file')
    #check if the post request has the file part
    if 'file' not in request.files:
        resp=jsonify({'message':'no file part in the request'})
        resp.status_code=400
        return resp
    file=request.files['file']
    if file.filename=='':
        resp=jsonify({'message':'No file selected for uploading'})
        resp.status_code=400
        return resp
    if file and allowed_file(file.filename):
        filename=secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
        _file_path=os.path.join(app.config['UPLOAD_FOLDER'],filename)
        try:
            if _file_path and request.method == 'POST':
                _assignmentname = request.get_data('assignmentname')
                _lecturername = request.get_data('_lecturername')
                _coursecode = request.get_data('_coursecode')
                _regnumber = request.get_data('_regnumber')
                _file = request.get_data('file')
                # save edits
                sql = "INSERT INTO assignments(assignmentname, lecturername,coursecode,url,regnumber) VALUES(%s,%s,%s,%s,%s)"
                data = (_assignmentname,_lecturername,_coursecode,_file,_regnumber)
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.execute(sql, data)
                conn.commit()
                resp=jsonify({'message':'Assignment Successfully Uploaded'})
                resp.status_code=201
                return resp
        except Exception as e:
            print(e)

        finally:
            cursor.close()
            conn.close()
    else:
        resp=jsonify({'message':'Allowed file type is pdf'})
        resp.status_code=40
        return resp

#student report
@app.route('/studentreport',methods = ['POST', 'GET'])
@cross_origin(origin='localhost',headers=['Content-Type','Authorisation'])
def studentPlagiarismResult():
   if request.method == 'POST':
      result=request.get_data('text')
      resp = jsonify(studentSimilarity.report(str(result)))
      return resp
   else:
    return not_found()

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found:' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp


if __name__ == "__main__":
        app.run(debug=True)