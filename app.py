from flask import *
app = Flask(__name__)
from crypt import verify_password,hash_password


#API -- Application Programming Interface
#CRUD--Create Read Update Delete
import pymysql
connection = pymysql.connect(host='localhost',user='root',password='',database='ecom')
@app.route('/profile/<int:customer_id>')
def profile(customer_id):
    try:

        cursor = connection.cursor(pymysql.cursors.DictCursor)
        sql= 'select * from customers where customer_id = %s'
        cursor.execute(sql,(customer_id))
        if cursor.rowcount > 0:
            record = cursor.fetchone()
            response = jsonify(record)
            response.status_code = 200
            return response
        else:
            response = jsonify({'msg': 'Not Found'})
            response.status_code = 404
            return response
    except Exception as e:
        response = jsonify({'msg': 'Error Occured'})
        response.status_code = 404
        return response

@app.route('/login', methods = ['POST'])
def login():
    try:
        json = request.json
        email = json['email']
        password = json['password']

        if email and password and request.method == 'POST':
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            sql = 'select * from customers where email = %s '
            cursor.execute(sql,(email))

            if cursor.rowcount == 0:
                response = jsonify({'msg': 'Email Not Found'})
                response.status_code = 404
                return response
            else:

                row = cursor.fetchone()
                hashed_password = row['password']
                # verify
                status = verify_password(hashed_password, password)
                if status == True:

                    response = jsonify(row)
                    response.status_code = 200
                    return response








                elif status == False:
                    response = jsonify({'msg': 'Login Failed'})
                    response.status_code = 404
                    return response
                else:
                    response = jsonify({'msg': 'Login Failed'})
                    response.status_code = 404
                    return response
        else:
            response = jsonify({'msg': 'Your Fields Are Empty'})
            response.status_code = 200
            return response
    except Exception as e:
            response = jsonify({'msg': 'Your Fields Are Empty'})
            response.status_code = 200
            return response

@app.route('/register', methods = ['POST'])
def register():
    try:
        json = request.json
        fname = json['fname']
        lname = json['lname']
        email = json['email']
        password = json['password']
        confirm_password = json['confirm_password']
        tel = json['tel']

        if len(fname) == 0:
            response = jsonify({'msg': 'Empty Firstname'})
            response.status_code = 302
            return response
        elif len(lname) == 0:
            response = jsonify({'msg': 'Empty Lastname'})
            response.status_code = 302
            return response
        elif len(email) == 0:
            response = jsonify({'msg': 'Empty Email'})
            response.status_code = 302
            return response
        elif len(tel) < 10:
            response = jsonify({'msg': 'Empty Phone Number'})
            response.status_code = 302
            return response
        elif len(password) < 8:
            response = jsonify({'msg': 'Telephone number should be atleast ten numbers'})
            response.status_code = 302
            return response
        if password != confirm_password:
            response = jsonify({'msg': 'Password Do Not Match'})
            response.status_code = 302
            return response

        else:
            cursor = connection.cursor(pymysql.cursors.DictCursor)
            sql = 'insert into customers(fname,lname,email,password,tel)values(%s,%s,%s,%s,%s) '
            try:

                cursor.execute(sql, (fname,lname,email,hash_password(password),tel))
                connection.commit()
                response = jsonify({'msg': 'Saved successful'})
                response.status_code = 302
                return response
            except:
                response = jsonify({'msg': 'Failed to save'})
                response.status_code = 302
                return response
    except:
        response = jsonify({'msg': 'Something Went Wrong'})
        response.status_code = 302
        return response

list10 = []
@app.route("/customer_pending_orders/<int:customer_id>")
def customer_pending_orders(customer_id):
            list10.clear()
            sql = 'select DISTINCT order_code from orders where email = %s and status = %s order by pay_date desc'
            cursor = connection.cursor()
            cursor.execute(sql, (customer_id, 'Pending'))
            if cursor.rowcount > 0:
                rows = cursor.fetchall()
                for row in rows:
                    sql4 = 'select * from orders where order_code = %s and status = %s order by pay_date desc'
                    cursor4 = connection.cursor(pymysql.cursors.DictCursor)
                    cursor4.execute(sql4, (row[0], 'Pending'))
                    rows = cursor4.fetchall()
                    list10.append(rows)
                response = jsonify(list10)
                response.status_code = 302
                return response
            else:
                response = jsonify({'msg':'No records'})
                response.status_code = 302
                return response





if __name__ == '__main__':
    app.run(port=6060)
    app.debug = True
