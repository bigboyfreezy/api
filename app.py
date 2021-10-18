from flask import *
app = Flask(__name__)
from crypt import verify_password


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




if __name__ == '__main__':
    app.run()
    app.debug = True
