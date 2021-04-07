# diagram.py
from diagrams import Cluster, Diagram
from diagrams.onprem.client import User
from diagrams.aws.compute import Lambda
from diagrams.aws.database import RDS
from diagrams.aws.mobile import APIGateway
from diagrams.aws.storage import S3


with Diagram("Moody's API Architecture", show=False):
    # ELB("lb") >> EC2("web") >> RDS("userdb") >> APIGateway("api")
    user = User("User")

    api = APIGateway("API Gateway")

    with Cluster("Lamba Function"):
        handlers = [Lambda("function1"),
                    Lambda("function2"),
                    Lambda("function3")]

    db_master = RDS("Datawarehouse")

    output = S3("Output")

    user >> api >> handlers >> db_master >> output