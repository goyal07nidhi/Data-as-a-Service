from diagrams import Cluster, Diagram
from diagrams.aws.storage import S3
from diagrams.saas.analytics import Snowflake
from diagrams.programming.framework import FastAPI
from diagrams.firebase.develop import Authentication
from diagrams.programming.flowchart import Preparation
from diagrams.onprem.workflow import Airflow
from diagrams.programming.flowchart import MultipleDocuments

with Diagram("API Architecture", show=False):

    airflow = Airflow("Airflow")

    with Cluster("Airflow Process"):
        input_data = MultipleDocuments("Input CSV's")
        prep = Preparation("Preprocess")
        with Cluster("Snowflake"):
            snowflake = Snowflake("Staging")
            database = Snowflake("Database")

    with Cluster("FastAPI"):
        with Cluster("Methods"):
            methods = [FastAPI("FastAPI Get"),
                       FastAPI("FastAPI Post")]

        auth = Authentication("Authenticate")
        fetch = Snowflake("Fetch Data")
        out = S3("Output")

    airflow >>input_data >> prep >> snowflake >> database >> methods >> auth >> fetch >> out
