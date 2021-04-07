from locust import HttpLocust, task, between, TaskSet


class UserBehaviour(TaskSet):
    @task(1)
    def docs_index(self):
        self.client.get("http://127.0.0.1:8080/")

    def all_data_index(self):
        self.client.get("http://127.0.0.1:8080/ProductionPlantData/ColumnNames?access_token=Team6")

    @task(2)
    def column_index(self):
        self.client.get("http://127.0.0.1:8080/ProductionPlantData/column/A_1%2C%20L_2?access_token=Team6")

    @task(3)
    def experiment_index(self):
        self.client.get("http://127.0.0.1:8080/ProductionPlantData/experiment/11?access_token=Team6")

    @task(4)
    def timestamp_index(self):
        self.client.get("http://127.0.0.1:8080/ProductionPlantData/timestamp/10000?access_token=Team6")

    @task(5)
    def feature_index(self):
        self.client.get("http://127.0.0.1:8080/ProductionPlantData/feature/feature_1?access_token=Team6")

    @task(6)
    def range_index(self):
        self.client.get("http://127.0.0.1:8080/ProductionPlantData/data_between/A_1/21/23?access_token=Team6")


'''
    @task(7)
    def post_index(self):
        self.client.post("http://127.0.0.1:8080/data-into-snowflake/v1?access_token=Team6")
'''


class WebsiteUser(HttpLocust):
    task_set = UserBehaviour
    wait_time = between(5, 9)

