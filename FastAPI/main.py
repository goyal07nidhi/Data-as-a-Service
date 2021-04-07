import uvicorn
from fastapi import Security, Depends, FastAPI, HTTPException, File, UploadFile
from fastapi.security.api_key import APIKeyQuery, APIKeyHeader, APIKey
from starlette.status import HTTP_403_FORBIDDEN
from pydantic import BaseModel
import snowflake.connector
from snowflake.connector import DictCursor
import shutil

API_KEY = "Team6"
API_KEY_NAME = "access_token"

# extract the access_token key in the query
api_key_query = APIKeyQuery(name=API_KEY_NAME, auto_error=False)
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

app = FastAPI()

features = {'feature_1': ['A_1', 'A_2', 'A_3', 'A_4', 'A_5'],
            'feature_2': ['B_1', 'B_2', 'B_3', 'B_4', 'B_5'],
            'feature_3': ['C_1', 'C_2', 'C_3', 'C_4', 'C_5'],
            'feature_4': ['L_1', 'L_2'],
            'feature_5': ['L_3', 'L_6'],
            'feature_6': ['L_4', 'L_5'],
            'feature_7': ['L_7', 'L_8'],
            'feature_8': ['L_9', 'L_10']}


class Item(BaseModel):
    experiment: int
    timestamp: int
    column: str
    data_greater_than: int
    data_less_than: int
    feature: str
    input: str


# defining API key
async def get_api_key(
        api_key_query: str = Security(api_key_query)):
    if api_key_query == API_KEY:
        return api_key_query
    else:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )


auto_error = False

global ctx
ctx = snowflake.connector.connect(user='username',
                                  password='userPassword',
                                  account='accountName',
                                  warehouse='warehouse',
                                  database='database',
                                  table='tableName',
                                  schema='PUBLIC',
                                  protocol='https')


@app.get("/", tags=["Welcome to Project Team 6"])
async def read_root():
    return {"Welcome to Team 6 Project Page": "Production Plant Data for Condition Monitoring"}


# Snowflake - Fetching all records
@app.get("/ProductionPlantData", tags=["Production Plant Data"])
async def fetch_all_data(api_key: APIKey = Depends(get_api_key)):
    if APIKey:
        # Create a cursor object.
        cur = ctx.cursor(DictCursor)

        sql = "SELECT * FROM PROD_PLANT LIMIT 5"
        query = cur.execute(sql)
        result = []
        for data in query:
            result.append(data)
        return result
    else:
        raise HTTPException(status_code=404, detail="Data not Found")


# Snowflake -Fetching columns information
@app.get("/ProductionPlantData/column/{column}", tags=["Column data of Production Plant"])
async def fetch_data_by_columns(column: str, api_key: APIKey = Depends(get_api_key)):
    if APIKey:
        try:
            # Create a cursor object.
            cur = ctx.cursor()
            sql = "select" + " " +column + " " +"from PROD_PLANT LIMIT 6;"
            cur.execute(sql)
            data = cur.fetch_pandas_all()
            return data
        except:
            raise HTTPException(status_code=404, detail="One or more columns not Found")


# Fetching records of particular experiment
@app.get("/ProductionPlantData/experiment/{experiment}", tags=["Production Plant Data by Experiment"])
async def get_data_by_experiment(experiment: int, api_key: APIKey = Depends(get_api_key)):
    if APIKey:
        # Create a cursor object.
        cur = ctx.cursor(DictCursor)

        if experiment in [7, 8, 9, 11, 13, 14, 15, 16]:
            sql = "select * from PROD_PLANT where EXPERIMENT_NUMBER = " + str(experiment) + " limit 2"
            query = cur.execute(sql)
            result = []
            for data in query:
                result.append(data)
            return result
        else:
            raise HTTPException(status_code=404, detail="Experiment Number not Found")


# Fetching records of particular timestamp
@app.get("/ProductionPlantData/timestamp/{timestamp}", tags=["Production Plant Data by Timestamp"])
async def get_data_by_timestamp(timestamp: int, api_key: APIKey = Depends(get_api_key)):
    if APIKey:
        # Create a cursor object.
        cur = ctx.cursor(DictCursor)

        sql = "select * from PROD_PLANT where TIMESTAMP = " + str(timestamp) + " limit 10"
        query = cur.execute(sql)
        result = []
        for data in query:
            result.append(data)
        if len(result) == 0:
            raise HTTPException(status_code=404, detail="Timestamp not Found")
        else:
            return result


# Fetching records of particular feature
@app.get("/ProductionPlantData/feature/{feature}", tags=["Production Plant Data by Features"])
async def get_data_by_feature(feature: str, api_key: APIKey = Depends(get_api_key)):
    if APIKey:
        try:
            # Create a cursor object.
            cur = ctx.cursor(DictCursor)

            string = ",".join(features[feature])
            sql = "select " + string + " from PROD_PLANT limit 3"
            query = cur.execute(sql)
            result = []
            for data in query:
                result.append(data)
            return result
        except:
            raise HTTPException(status_code=404, detail="Feature not Found")


# Fetching records of between particular timestamp
@app.get("/ProductionPlantData/data_between/{column_name}/{data_greater_than}/{data_less_than}",
         tags=["Production Plant Data by Range"])
async def get_data_between_range(column_name: str, data_greater_than: int, data_less_than: int,
                                 api_key: APIKey = Depends(get_api_key)):
    if APIKey:
        # Create a cursor object.
        cur = ctx.cursor(DictCursor)

        try:
            sql = "select * " \
                  "from PROD_PLANT " \
                  "where " + column_name + " >=" + str(data_greater_than) + "and " + column_name + " <= " + str(data_less_than) + \
                  " limit 5"
            query = cur.execute(sql)
            result = []
            for data in query:
                result.append(data)
            return result
        except:
            raise HTTPException(status_code=404, detail="Variables not Found")


@app.post("/data-into-snowflake/v1", tags=["Push CSV data into Snowflake"])
async def push_data_into_snowflake(file: UploadFile = File(...), api_key: APIKey = Depends(get_api_key)):
    with open("load-data-into-snowflake.csv", "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    if APIKey:
        # Create a cursor object.
        cur = ctx.cursor()
        sql = "PUT file:///Users/ng/Downloads/CSYE7245_NidhiGoyal/Assignment_3/FastAPI/load-data-into-snowflake.csv @%PROD_PLANT"
        cur.execute(sql)
    return {"result": "Import successful"}


if __name__ == '__main__':
    uvicorn.run(app, port=8080, host='127.0.0.1')
