import requests
import matplotlib.pyplot as plt
import sys


class NotionSync:
    def __init__(self):
        pass

    def query_database(self, integration_token, database_id):
        database_url = "https://api.notion.com/v1/databases/" + database_id + "/query"
        response = requests.post(database_url,
                                 headers={"Authorization": f"{integration_token}", "Notion-Version": "2022-06-28"})
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
data = nsync.query_database(sys.argv[1], sys.argv[2])
ticket_stats = nsync.get_ticket_data(data)

fig, ax = plt.subplots()
labels = "Automated", "To-Do", "In Progress"
ax.pie(ticket_stats, labels=labels, autopct="%1.1f%%")
plt.savefig("graph.png")