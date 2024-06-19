"""
Database Connection Module
--------------------------
This module provides a function to connect to a MySQL database using
environment variables for the connection parameters. 

It loads the environment variables from a .env file and returns a 
MySQL connection object.

To Do:
- Change the connection handling to support hosting the app in different environments.
"""

import os
from dotenv import load_dotenv
import mysql.connector

def mysql_db_connect() -> mysql.connector.MySQLConnection:
    """
    Establishes a connection to a MySQL database using environment variables.

    Returns:
        mysql.connector.MySQLConnection: A connection object to the MySQL database.
    """
    # Load environment variables from .env file
    load_dotenv()

    # Connect to MySQL
    connection = mysql.connector.connect(
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        port=os.getenv("DB_PORT")
    )

    return connection
