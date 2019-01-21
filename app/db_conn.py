"""Database Class for all db related functions"""
import os
import psycopg2 as pg2

db_url = os.getenv('DATABASE_URL')
# url = "dbname='questioner' host='localhost' port='5432' user='postgres' password='@Yonknapatwa1'"

def init_connection(db_url):
    """Function to connect to db through psycopg"""
    conn = pg2.connect(db_url)
    return conn

def get_connection():
    """Function to initialize the database"""
    db = init_connection(db_url)
    return db

def create_tables():
    """Function to create tables if the do not exist"""
    conn = init_connection(db_url)
    curr = conn.cursor()
    tables = db_tables()

    for query in tables:
        curr.execute(query)
    conn.commit()


def db_tables():
    """Queries to create app tables"""
    tbl1 = """CREATE TABLE IF NOT EXISTS meetups (
        meetup_id serial PRIMARY KEY NOT NULL,
        created_by INT NOT NULL,
        location CHAR(50) NOT NULL,
        topic CHAR(50) NULL,
        images CHAR(50) NULL
        )"""

    tbl2 = """CREATE TABLE IF NOT EXISTS questions (
        question_id serial PRIMARY KEY NOT NULL,
        meetup_id INT NOT NULL,
        user_id INT NOT NULL,
        title CHAR(100) NOT NULL,
        body CHAR(150) NOT NULL
        )"""

    tbl3 = """CREATE TABLE IF NOT EXISTS comments (
        comment_id serial PRIMARY KEY NOT NULL,
        question_id INT NOT NULL,
        user_id INT NOT NULL,
        comment CHAR(150) NOT NULL
        )"""

    tbl4 = """CREATE TABLE IF NOT EXISTS rsvp (
        rsvp_id serial PRIMARY KEY NOT NULL,
        meetup_id INT NOT NULL,
        user_id INT NOT NULL,
        status CHAR(10) NOT NULL
        )"""

    tbl5 = """CREATE TABLE IF NOT EXISTS users (
        user_id serial PRIMARY KEY NOT NULL,
        firstname CHAR(40) NOT NULL,
        lastname CHAR(45) NOT NULL,
        email CHAR(45) NOT NULL,
        created_on CHAR(50) NOT NULL,
        is_admin BOOLEAN NOT NULL DEFAULT FALSE,
        password CHAR(150) NOT NULL,
        username CHAR(20) NULL
        )"""

    tables = [tbl1, tbl2, tbl3, tbl4, tbl5]
    return tables
