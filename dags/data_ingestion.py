# Imports the modules
import os
import json
import pandas as pd
import snowflake.connector
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.utils.dates import days_ago

Data_dir = "/Users/ng/Downloads/CSYE7245_NidhiGoyal/Assignment_3/Production_Plant_data_input"
prod_df = pd.DataFrame()
conn = None


def read_input():
    df_list = []
    file_dict = {'C11.csv': 11, 'C16.csv': 16, 'C15.csv': 15, 'C14.csv': 14, 'C13-1.csv': 13, 'C13-2.csv': 13,
                 'C7-1.csv': 7, 'C9.csv': 9, 'C7-2.csv': 7, 'C8.csv': 8}
    for file in os.listdir(Data_dir):
        exp_no = file_dict[file]
        df = pd.read_csv(Data_dir + '/' + file, error_bad_lines=False, low_memory=False, delimiter=',')
        df['experiment_number'] = exp_no
        df_list.append(df)

    prod_df = pd.concat(df_list)
    prod_df.reset_index(drop=True, inplace=True)
    return prod_df.to_json()


def preprocess(task_instance):
    json_str = task_instance.xcom_pull(task_ids='ReadInput')
    json_obj = json.loads(json_str)
    prod_df = pd.DataFrame.from_dict(json_obj)
    prod_df.dropna(inplace=True)
    print(prod_df.shape)
    prod_df.drop_duplicates(inplace=True)
    prod_df.columns = [x.upper() for x in prod_df.columns]
    return prod_df.to_json()


def df_to_csv(task_instance):
    json_str = task_instance.xcom_pull(task_ids='ReadInput')
    json_obj = json.loads(json_str)
    prod_df = pd.DataFrame.from_dict(json_obj)
    prod_df.to_csv(Data_dir + '.csv', index=False, header=False)


def snowflake_connection():
    global conn
    # Insert snowflake credentials
    conn = snowflake.connector.connect(user='username',
                                       password='userPassword',
                                       account='accountName')
    print('Snowflake Connection established!')


def snowflake_setup():
    global conn
    if conn is None:
        snowflake_connection()

    cur = conn.cursor()
    # Starting with the Role.
    sql = "USE ROLE SYSADMIN"
    cur.execute(sql)

    # Define warehouse and use it.
    sql = "CREATE WAREHOUSE IF NOT EXISTS MY_WH " \
          "WITH WAREHOUSE_SIZE = SMALL"
    cur.execute(sql)
    sql = "USE WAREHOUSE MY_WH"
    cur.execute(sql)

    # Create database and use it
    sql = "CREATE DATABASE IF NOT EXISTS ASSIGNMENT_3"
    cur.execute(sql)
    sql = "USE DATABASE ASSIGNMENT_3"
    cur.execute(sql)

    # Create and use schema.
    sql = "CREATE SCHEMA IF NOT EXISTS PUBLIC"
    cur.execute(sql)
    sql = "USE SCHEMA PUBLIC"
    cur.execute(sql)

    # Create and use schema.
    sql = "create or replace stage PROD_PLANT " \
          "file_format = MY_CSV_FORMAT"
    cur.execute(sql)

    # Close the cursor
    cur.close()


def snowflake_as_staging():
    global conn
    if conn is None:
        snowflake_setup()

    cur = conn.cursor()

    # Remove the previous stage data
    sql = "REMOVE @%PROD_PLANT"
    cur.execute(sql)
    # Put csv files into snowflake staging
    sql = "PUT file:///Users/ng/Downloads/CSYE7245_NidhiGoyal/Assignment_3/Production_Plant_data_input.csv* @%PROD_PLANT"
    cur.execute(sql)


def import_data_into_snowflake_db():
    global conn
    if conn is None:
        snowflake_setup()

    cur = conn.cursor()
    # Truncate the previous load
    sql = "TRUNCATE TABLE PROD_PLANT"
    cur.execute(sql)

    # Copy the data from staging to snowflake table
    sql = "COPY INTO PROD_PLANT"
    cur.execute(sql)


default_args = {
    'owner': 'airflow',
    'start_date': days_ago(0),
    'concurrency': 1,
    'retries': 0,
    'depends_on_past': False,
}

with DAG('Data_Ingestion',
         catchup=False,
         default_args=default_args,
         schedule_interval='@once',
         ) as dag:
    t0_start = PythonOperator(task_id='ReadInput',
                              python_callable=read_input)
    t1_preprocess = PythonOperator(task_id='Preprocess',
                                   python_callable=preprocess,
                                   provide_context=True)
    t2_csv = PythonOperator(task_id='CSVForm',
                            python_callable=df_to_csv,
                            provide_context=True)
    t3_connection = PythonOperator(task_id='SnowflakeConnection',
                                   python_callable=snowflake_connection)
    t4_setup = PythonOperator(task_id='SnowflakeSetup',
                              python_callable=snowflake_setup)
    t5_stage = PythonOperator(task_id='SnowflakeStaging',
                              python_callable=snowflake_as_staging)
    t6_import = PythonOperator(task_id='DataIngestionIntoSnowflake',
                               python_callable=import_data_into_snowflake_db)

t0_start >> t1_preprocess >> t2_csv >> t3_connection >> t4_setup >> t5_stage >> t6_import
