from fastapi.testclient import TestClient
from fastapi import Depends
from fastapi.security.api_key import APIKey
from main import app, get_api_key
import os

client = TestClient(app)


def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"Welcome to Team 6 Project Page": "Production Plant Data for Condition Monitoring"}


def test_fetch_all_data(api_key: APIKey = Depends(get_api_key)):
    response = client.get("/ProductionPlantData?access_token=Team6")
    assert response.status_code == 200
    assert len(response.json()) == 5


def test_fetch_data_by_columns(api_key: APIKey = Depends(get_api_key)):
    column = "A_1"
    response = client.get("/ProductionPlantData/column/{}?access_token=Team6".format(column))
    assert response.status_code == 200
    assert (column in response.json().keys()) == True
    assert len(response.json()[column]) == 6


def test_get_data_by_experiment(api_key: APIKey = Depends(get_api_key)):
    experiment = 7
    response = client.get("/ProductionPlantData/experiment/{}?access_token=Team6".format(experiment))
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_get_data_by_timestamp(api_key: APIKey = Depends(get_api_key)):
    timestamp = 22
    response = client.get("/ProductionPlantData/timestamp/{}?access_token=Team6".format(timestamp))
    assert response.status_code == 200
    assert len(response.json()) == 10


def test_get_data_by_feature(api_key: APIKey = Depends(get_api_key)):
    feature = 'feature_1'
    response = client.get("/ProductionPlantData/feature/{}?access_token=Team6".format(feature))
    assert response.status_code == 200
    assert len(response.json()) == 3


def test_get_data_between_range(api_key: APIKey = Depends(get_api_key)):
    column_name = 'A_1'
    data_greater_than = 23
    data_less_than = 33
    response = client.get("/ProductionPlantData/data_between/{0}/{1}/{2}?access_token=Team6".format(column_name, data_greater_than, data_less_than))
    assert response.status_code == 200
    assert len(response.json()) == 5
