from flask import Flask, render_template, request
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

@app.route("/samplepage", methods=['GET', 'POST'])
def samplepage():
    return render_template('samplepage.html')

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
    with connections.Connection(
        host=customhost,
        port=3306,
        user=customuser,
        password=custompass,
        db=customdb
    ) as db_conn:
        emp_id = request.form['emp_id']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        pri_skill = request.form['pri_skill']
        location = request.form['location']
        emp_image_file = request.files['emp_image_file']

        insert_sql = "INSERT INTO employee VALUES (%s, %s, %s, %s, %s)"
        cursor = db_conn.cursor()

        if emp_image_file.filename == "":
            return "Please select a file"

        try:

            cursor.execute(insert_sql, (emp_id, first_name,
                           last_name, pri_skill, location))
            db_conn.commit()
            emp_name = "" + first_name + " " + last_name
            # Uplaod image file in S3 #
            emp_image_file_name_in_s3 = "emp-id-" + str(emp_id) + "_image_file"
            s3 = boto3.resource('s3')

            try:
                print("Data inserted in MySQL RDS... uploading image to S3...")
                s3.Bucket(custombucket).put_object(
                    Key=emp_image_file_name_in_s3, Body=emp_image_file)
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
        return render_template('AddEmpOutput.html', name=emp_name)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
