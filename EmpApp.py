from flask import Flask, render_template, request,make_response
from pymysql import connections
import os
import boto3
from config import *

app = Flask(__name__)

bucket = custombucket
region = customregion
output = {}
table = 'employee'


@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route("/addEmp", methods=['GET', 'POST'])
def addEmp():
    return render_template('addEmp.html')

# @app.route("/addingEmployee", methods=['GET', 'POST'])
# def addingEmployee():
#     first_name = request.form.get("first_name")
#     last_name = request.form.get("last_name")
#     if first_name!="":
#         full_name = "" + first_name + " " + last_name
#     else:
#         full_name = "The employee"

#     return render_template('addSuccessful.html',full_name=full_name)  

@app.route("/addSuccessful", methods=['GET', 'POST'])
def addSuccessful():    
    return render_template('addSuccessful.html')

@app.route("/empDetails", methods=['GET', 'POST'])
def empDetails():
    return render_template('empDetails.html')

@app.route("/retrieveEmp", methods=['GET', 'POST'])
def retrieveEmp():
    return render_template('retrieveEmp.html')

@app.route("/samplepage", methods=['GET', 'POST'])
def samplepage():
    return render_template('samplepage.html')

@app.route("/searchEmployee", methods=['GET', 'POST'])
def searchEmployee():
    
    with connections.Connection(
        host=customhost,
        port=3306,
        user=customuser,
        password=custompass,
        db=customdb
    ) as db_conn:
        emp_id = request.form['emp_id']

        select_sql = "SELECT * FROM employee WHERE emp_id = %s"
        cursor = db_conn.cursor()
        cursor.execute(select_sql,(emp_id))

        records = cursor.fetchall()
        row_count = cursor.rowcount
        if row_count!=0:
            
            global emp_id1
            global first_name1
            global last_name1
            global pri_skill1
            global location1
            global image_url1
                
            for row in records:
                
                emp_id1 = row[0]
                first_name1 = row[1]
                last_name1 = row[2]
                pri_skill1 = row[3]
                location1 = row[4]

        cursor.close()
        image_url1 = str("https://chongkewei-bucket.s3.amazonaws.com/emp-id-") + str(emp_id1) + str("_image_file.png")
        # s3 = boto3.resource('s3')
        # s3_client = boto3.client('s3')
        # public_urls = []
        # file_path = "emp-id-" + str(emp_id1) + "_image_file"
        # try:
        #     for item in s3_client.list_objects(Bucket=bucket)['Contents']:
        #         presigned_url = s3_client.generate_presigned_url('get_object', Params = {'Bucket': bucket, 'Key': item[file_path]})
        #         public_urls.append(presigned_url)
        # except Exception as e:
        #     pass
       
        # img_url1 = public_urls

        # s3 = boto3.resource('s3')
        # file_path = "emp-id-" + str(emp_id1) + "_image_file"
        # try:
        #     image = s3.Object(custombucket, file_path).get()["Body"].read()
        # except Exception as e:
        #     return {"status": -1, "msg": str(e)}
        # response = make_response(image)
        # response.headers.set('Content-Type', 'image/png')
        # response.headers.set(
        #     'Content-Disposition', 'attachment', filename='%s.png' % file_path)


        return render_template('empDetails.html', emp_id=emp_id1,first_name=first_name1,last_name=last_name1,pri_skill=pri_skill1,location=location1,img_url=image_url1)

@app.route("/passPOSTDataSample", methods=["GET", "POST"])
def passPOSTDataSample():
    field1 = request.form.get("field1")
    field2 = request.form.get("field2")

    output = ""
    if field1 is not None:
        output += "field1: " + field1 + "<br>"
    if field2 is not None:
        output += "field2: " + field2 + "<br>" 

    return render_template('passPOSTDataSample.html', my_display_data="something something html", previous_form_data=output)


@app.route("/addEmployee", methods=['POST'])
def AddEmp():
    global emp_id2
    global first_name2
    global last_name2
    global pri_skill2
    global location2
    global emp_image_file2
    
    with connections.Connection(
        host=customhost,
        port=3306,
        user=customuser,
        password=custompass,
        db=customdb
    ) as db_conn:
        emp_id2 = request.form['emp_id']
        first_name2 = request.form['first_name']
        last_name2 = request.form['last_name']
        pri_skill2 = request.form['pri_skill']
        location2 = request.form['location']
        emp_image_file2 = request.files['emp_image_file']

        insert_sql = "INSERT INTO employee VALUES (%s, %s, %s, %s, %s)"
        cursor = db_conn.cursor()

        if emp_image_file2.filename == "":
            return "Please select a file"

        try:

            cursor.execute(insert_sql, (emp_id2, first_name2,
                           last_name2, pri_skill2, location2))
            db_conn.commit()
            full_name = "" + first_name2 + " " + last_name2
            # Upload image file in S3 #
            emp_image_file_name_in_s3 = "emp-id-" + str(emp_id2) + "_image_file" + str(".png")
            s3 = boto3.resource('s3')

            try:
                print("Data inserted in MySQL RDS... uploading image to S3...")
                s3.Bucket(custombucket).put_object(
                    Key=emp_image_file_name_in_s3, Body=emp_image_file2, ContentType='image/png')
                bucket_location = boto3.client(
                    's3').get_bucket_location(Bucket=custombucket)
                s3_location = (bucket_location['LocationConstraint'])

                if s3_location is None:
                    s3_location = ''
                else:
                    s3_location = '-' + s3_location

                object_url = "https://s3{0}.amazonaws.com/{1}/{2}".format(
                    s3_location,
                    custombucket,
                    emp_image_file_name_in_s3)

            except Exception as e:
                return str(e)

        finally:
            cursor.close()

        print("all modification done...")
        return render_template('addSuccessful.html', full_name=full_name)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
