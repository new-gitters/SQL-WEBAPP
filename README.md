# SQL-WEBAPP
This is a flask web application to run sql query and show the result

#To run the program, the virtual enviroment has to be set with Python 3.5+ and Flask installed


Nginx virtual server setting:

directory /etc/nginx/conf.d/
virtual.conf 
This file contains the settings for the port number and public ip address.
The ip address is #.##.###.##
port:80

To run the nginx server just type: sudo service nginx restart

Then to run the flask app 
Redirect to the ~/flaskapp directory and type the command:gunicorn app:app

The index.html is stored in the templates folder.
