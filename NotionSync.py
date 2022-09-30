import os
import requests
import matplotlib.pyplot as plt


INTEGRATION_KEY = os.environ.get("INTEGRATION_TOKEN")
DATABASE_ID = os.environ.get("TICKET_DATABASE_ID")


class NotionSync:
    def __init__(self):
        pass

    def query_database(self, database_id):
        database_url = "https://api.notion.com/v1/databases/" + database_id + "/query"
        response = requests.post(database_url,
                                 headers={"Authorization": f"{INTEGRATION_KEY}", "Notion-Version": "2022-06-28"})
        if response.status_code != 200:
            raise Exception(f'Response Status: {response.status_code}')
        else:
            return response.json()

    def get_ticket_data(self, data_json):
        automated = to_do = in_progress = 0
        for ticket in data_json["results"]:
            if ticket["properties"]["Status"]["status"]["name"] == "Automated":
                automated += 1
            elif ticket["properties"]["Status"]["status"]["name"] == "To-Do":
                to_do += 1
            elif ticket["properties"]["Status"]["status"]["name"] == "In Progress":
                in_progress += 1
            else:
                raise Exception("No such status")
        return [automated, to_do, in_progress]


nsync = NotionSync()
data = nsync.query_database("03e543a528c7412f9c5c9bc315320e98")
ticket_stats = nsync.get_ticket_data(data)

fig, ax = plt.subplots()
labels = "Automated", "To-Do", "In Progress"
ax.pie(ticket_stats, labels=labels, autopct="%1.1f%%")
plt.savefig("graph.png")
