# Data-as-a-service

[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)


#### Quick Links

- [CLAAT document](https://codelabs-preview.appspot.com/?file_id=1M2o9u5VdoHaRgmlBjQgv8Zi6T40cagB8ZHCO2lpLaBo#0)


---
## Getting Started
The Goal of this project is to build an application for a company who is interested in monetizing it’s data and making it’s data available as an API. 
To build this service, we are using Fast API to illustrate how it works.

## Data used:

- https://www.kaggle.com/inIT-OWL/production-plant-data-for-condition-monitoring

## Task performed

- Task 1: Review
- Task 2: Data Ingestion
- Task 3: Design the Fast API
- Task 4: Enabling API key authentication
- Task 5: Test API

## Project Structure
```
Assignment_3/
├── dags/
│   └── data_ingestion.py
├── FastAPI/
│   ├── main.py
│   └── test_main.py
├── locust_load_test.py
├── MindiagramArchitecture/
│   ├── datalytics_architecture.py
│   └── moody_architecture.py
├── Production_Plant_data_input/
│   ├── C11.csv
│   ├── C13-1.csv
│   ├── C13-2.csv
│   ├── C14.csv
│   ├── C15.csv
│   ├── C16.csv
│   ├── C7-1.csv
│   ├── C7-2.csv
│   ├── C8.csv
│   └── C9.csv
├── README.md
└── TestingJupyterNotebook/
    ├── main.ipynb
    └── test_main.ipynb
```
## Task 1: Review

![api_architecture](https://user-images.githubusercontent.com/56357740/113388635-9752ea80-935c-11eb-8c83-d4e4c6aea2f8.png)

### Setup:
1. install chocolatey 
2. Run ```choco install graphviz``` in administer mode for windows
3. Run the code in administer mode in PowerShell
```
Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))
```
4. pip install diagrams

### Process:
1. Make a .py based on your architecture and run the file. An image should be created in the path of your python file

## Task 2: Data Ingestion

<img width="560" alt="Screen Shot 2021-03-31 at 3 12 36 PM" src="https://user-images.githubusercontent.com/56357740/113198140-8eb2c500-9233-11eb-9bea-811c9e5ec3d5.png">

### Requirements:
- Snowflake
- Airflow

#### 1. Snowflake Account Setup
Create a snowflake account by using below link:
```
https://signup.snowflake.com/?_ga=2.124938569.258300955.1617216030-578664637.1617216030
```
#### 2. Snowflake connection setup: 
To verify your version of Python:
```
python --version
```
Use pip version 19.0 or later. Execute the following command to ensure the required version is installed:
```
python -m pip install --upgrade pip
```
To install the connector, run the following commands:
```
pip install snowflake-connector-python==<version>
pip install —upgrade snowflake-connector-python
```
Verify your installation
Create a file (e.g. validate.py) containing the following Python sample code, which connects to Snowflake and displays the Snowflake version:
```
#!/usr/bin/env python
import snowflake.connector

Gets the version
ctx = snowflake.connector.connect( user='<user_name>', password='<password>', account='<account_name>')
cs = ctx.cursor()
try:
    cs.execute("SELECT current_version()")
    one_row = cs.fetchone()
    print(one_row[0])
finally:
    cs.close()
ctx.close()
```
>:Note: Make sure to replace <user_name>, <password>, and <account_name> with the appropriate values for your Snowflake account.

Next, execute the sample code by:
```
python validate.py
```
#### 3. Airflow setup:
```
pip install apache-airflow
pip install -r requirements.txt
```
Once Airflow is installed, configure the same by running:
```
# Use your present working directory as the airflow home
export AIRFLOW_HOME=~(pwd)

# export Python Path to allow use of custom modules by Airflow
export PYTHONPATH="${PYTHONPATH}:${AIRFLOW_HOME}"

# initialize the database
airflow db init

airflow users create \
    --username admin \
    --firstname <YourName> \
    --lastname <YourLastName> \
    --role Admin \
    --email example@example.com
```

#### 4. Using Airflow
Start the Airflow server in daemon
```
airflow webserver -D
```
Start the Airflow Scheduler
```
airflow scheduler
```
Once both are running - you should be able to access the Airflow UI by visiting http://127.0.0.1:8080/home on your browser.

To kill the Airflow webserver daemon:
```
lsof -i tcp:8080  
```
You should see a list of all processes that looks like this:
```
COMMAND   PID USER   FD   TYPE             DEVICE SIZE/OFF NODE NAME
Python  24905   ng    6u  IPv4 0x4b0a093c5550948f      0t0  TCP *:http-alt (LISTEN)
Python  24909   ng    6u  IPv4 0x4b0a093c5550948f      0t0  TCP *:http-alt (LISTEN)
Python  24911   ng    6u  IPv4 0x4b0a093c5550948f      0t0  TCP *:http-alt (LISTEN)
Python  24912   ng    6u  IPv4 0x4b0a093c5550948f      0t0  TCP *:http-alt (LISTEN)
Python  24916   ng    6u  IPv4 0x4b0a093c5550948f      0t0  TCP *:http-alt (LISTEN)
Python  24923   ng    6u  IPv4 0x4b0a093c5550948f      0t0  TCP *:http-alt (LISTEN)

```
Kill the process by running kill <PID> - in this case, it would be kill 24905

#### Running the Pipeline
Login to Airflow on your browser and turn on the Data_Ingestion DAG from the UI. Start the pipeline by choosing the DAG and clicking on Run.

![113389409-fb29e300-935d-11eb-8ea](https://user-images.githubusercontent.com/33648410/113392485-337ff000-9363-11eb-9424-ca7bcaa35d91.gif)

## Task 3: Design the Fast API

#### Requirements:
- Fastapi
- Pytest

#### Fastapi setup:
Install FastAPI framework, high performance, easy to learn, fast to code, ready for production
```
pip install fastapi
```
Install the lightning-fast ASGI server Uvicorn
```
pip install uvicorn
```
Install Python snowflake connector to get data from snowflake or post data into snowflake
```
pip install snowflake-connector-python==<version>
```
Simple powerful testing with python
```
pip install pytest
```
>:Note: Make sure to replace <user_name>, <password>,<account_name>,<warehouse>, <database>,<table> and <schema> with the appropriate values for your Snowflake account



Built various API's that can be used to query different aspects of the dataset.

Create various GET and POST methods using FastApi

Review https://fastapi.tiangolo.com/tutorial/ for an intro to API


#### Using Fastapi:

 

Go to the Fastapi DIrectory path and you will see two files main.py and test_main.py
```
http://localhost:8080/
```
You can now run uvicorn main:app --reload to start fastapi running on 8080 port.

 

#### Using Pytest:

 

To check whether our api is working well, we can use make use of test_main.py file by simply running pytest

In that, we have our Test Client defined to test all the api's present in our app

## Task 4:  Enabling API key authentication

To enable API key authentication

We refered https://medium.com/data-rebels/fastapi-authentication-revisited-enabling-api-key-authentication-122dc5975680


#### Authentication Setup:
```
from fastapi.security.api_key import APIKeyQuery
```

-Set a API KEY name for instance to access_token


-Set a API Key to "Team6" for instance


#### Extract the access_token key in the query

Using the following line of code 
```
api_key_query = APIKeyQuery(name=API_KEY_NAME, auto_error=False)
```

#### Define the API Key
```
async def get_api_key(
        api_key_query: str = Security(api_key_query)):
    if api_key_query == API_KEY:
        return api_key_query
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )
```


- Call this api key function from each and every api function to authenticate it

## Task 5: Test API
### Test Unit Cases
#### Setup: 
Install PyTest by running this:
```
 % pip install pytest
```
#### Using TestClient

Import ```TestClient```
Create a ```TestClient``` passing to it your ```FastAPI```.

Create functions with a name that starts with ```test.``` (this is standard pytest conventions).

Use the ```TestClient``` object the same way as you do with requests.

Write simple assert statements with the standard Python expressions that you need to check (again, standard pytest).
###### Run the command to test all use cases in test_main.py,
```
pytest or pytest -v
```

### Locust Load Test
#### Setup:

1.Install the libraries
```
pip install locustio==0.14.6
pip install greenlet==0.4.16
```
2. Run ```locust --help``` and should give you an output similar below
![image](https://user-images.githubusercontent.com/33648410/113393737-1815e480-9365-11eb-912d-7d8ed32a9822.png)
#### Process:

1. Make a .py file similar to locust_load_test.py to test the load test 

2. To run the file 
```
locust -f query_locust.py
```
3. Open the browser and enter the following url
```
http://localhost:8089/
```

4. Fill up the Number of users to simulate, Hatch rate, Host and click Start swarming 


## Team Members:

1. Nidhi Goyal
2. Kanika Damodarsingh Negi
3. Rishvita Reddy Bhumireddy


## Citation:

- https://github.com/mingrammer/diagrams
- https://docs.snowflake.com/en/user-guide/python-connector-example.html
- https://interworks.com/blog/chastie/2019/12/05/zero-to-snowflake-staging-explained/
- https://docs.snowflake.com/en/user-guide/data-load-local-file-system-create-stage.html                                   
- https://medium.com/data-rebels/fastapi-authentication-revisited-enabling-api-key-authentication-122dc5975680
- https://fastapi.tiangolo.com/tutorial/
- https://fastapi.tiangolo.com/tutorial/testing/
