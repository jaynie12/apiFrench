import notionKey
import requests
import os
import json

SECRET_KEY = notionKey.notion_key()
DATABASE_ID = notionKey.database_id()
#basic headers to set up the request
HEADERS =  {'Authorization': f"Bearer {SECRET_KEY}", 

           'Content-Type': 'application/json', 
           'Notion-Version': '2022-06-28'}
class DatabaseConnection:
    """
    Ability to connect to notion api
    """
    def __init__(self,secret_key, notion_headers, database_id):
        self.notion_key = secret_key
        self.notion_headers = notion_headers
        self.database_id = database_id

    #finding everything tied to my integration
    def response_search(self):
        json_search_param = {"filter": {"value": "page", "property": "object"}}
        search_response = requests.post(f'https://api.notion.com/v1/search', json=json_search_param, headers=self.notion_headers)
        return search_response.json()
    
    #post request
    def create_page(self, data: dict):
        create_url = "https://api.notion.com/v1/pages"
        # parent = the database where the new page is inserted, represented as a JSON object with a page_id or database_id key, and the corresponding ID.

        payload = {"parent": {"database_id": self.database_id}, "properties": data}

        res = requests.post(create_url, headers=self.notion_headers, json=payload)
        # print(res.status_code)
        return res

    def query_database(self):
            db_id = self.database_id
            url = f"https://api.notion.com/v1/databases/{db_id}/query"





# answer = DatabaseConnection(SECRET_KEY,HEADERS).response_search()

#answer = DatabaseConnection(SECRET_KEY,HEADERS).create_page()

# print(answer)