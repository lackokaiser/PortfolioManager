from flask import Flask, jsonify, session, request,render_template, g, redirect, url_for, flash
from flask_restful import Resource, Api,fields
import json
import mysql.connector

app = Flask("api")
api = Api(app)

@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

# New functions
@app.route("/portfolio")
def about():
    return render_template("portfolio_view.html")

@app.route("/history")
def history():
    return render_template("history.html")

# Global database connection for the service lifetime
def dbconn():
    try: 
        global password_db
        password_db = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "n3u3da!",
            database = "CSFoundation"
        )
        print(password_db)
    except Exception as e:
        print(f"Error connecting to database {e}")
        
        # restful api method of getting data
    
class getPortfolio(Resource):
    # Adding the default get method
    def get(self):
        passCursor = password_db.cursor(dictionary=True)
        passCursor.execute("SELECT * FROM stockdemotwo")
        passwords = passCursor.fetchall()
        passCursor.close()
        return jsonify(passwords)

    def post(self):
        data = json.loads(request.get_data())
        passCursor = password_db.cursor(dictionary=True)
        sqlstmt= '''INSERT INTO stockdemotwo (Name, Password) VALUES (%s, %s)'''
        passCursor.execute(sqlstmt, (data['name'],data['password']))
        passCursor.close()
        return data,201
    
    def put(self):
        data = json.loads(request.get_data())
        passCursor = password_db.cursor(dictionary=True)
        sqlstmt= '''UPDATE stockdemotwo SET Name = %s, password = %s WHERE loginid = %s'''
        passCursor.execute(sqlstmt, (data['name'], data['password']))
        passCursor.close()
        return data, 200

api.add_resource(getPortfolio, '/api/portfolio')

if __name__ == "__main__":
    dbconn()
    try:
        app.run(debug=True, host="0.0.0.0")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        # Close the database connection when the application terminates
        password_db.close()

