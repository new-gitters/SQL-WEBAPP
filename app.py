from flask import (
    Flask, redirect, render_template, request, url_for
)
from flaskext.mysql import MySQL
import pandas as pd
import psycopg2
import time
import os

app = Flask(__name__)

mysql = MySQL()

app.config['MYSQL_DATABASE_HOST'] = 'rucs527-db-instance.ceyuzmwfepll.us-east-2.rds.amazonaws.com'
app.config['MYSQL_DATABASE_USER'] = 'admin'
app.config['MYSQL_DATABASE_PASSWORD'] = 'cs527cs527'
app.config['MYSQL_DATABASE_DB'] = 'instacart'

mysql.init_app(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        statement = request.form['sql']
        df = pd.DataFrame()
        if request.form['db_choice'] == 'MySQL':
            conn = mysql.connect()
            cur = conn.cursor()
            cur.execute("SET  profiling = 1;")
            try:
                df = pd.read_sql_query(statement, con = conn )
            except TypeError:
                conn.commit()
            except Exception as error:
                cur.close()
                conn.close()
                return render_template('index.html', error=str(error))
            profiles = pd.read_sql_query("SHOW PROFILES;", con = conn )
            #print(profiles['Query'],profiles['Duration'])
            cur.close()
            conn.close()
            return render_template('index.html', tables=[df.to_html(classes='"table table-hover"', header=True,index=False)], elapsed=str(profiles['Duration'].values[0])+' seconds')
        elif request.form['db_choice'] == 'Redshift':
            conn = psycopg2.connect("dbname='instacart' port='5439' user='admin' password='CS527cs527' host='redshift-cluster-rucs527.czx9wj0j3pcw.us-east-2.redshift.amazonaws.com'")
            start_time = time.time()
            try: 
                df = pd.read_sql_query(statement, con = conn )
                end_time = time.time()
            except TypeError:
                end_time = time.time()
                conn.commit()
            except Exception as error:
                conn.close()
                return render_template('index.html', error=str(error))
            conn.close()
            return render_template('index.html', tables=[df.to_html(classes='"table table-hover"', header=True,index=False)], elapsed=str(round(end_time-start_time,8))+' seconds')

    return render_template('index.html')

if __name__ == '__main__':
    app.run()
