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
        self.page_id=None

    #finding everything tied to my integration
    def response_search(self):
        json_search_param = {"filter": {"value": "page", "property": "object"}}
        search_response = requests.post(f'https://api.notion.com/v1/search', json=json_search_param, headers=self.notion_headers)
        self.page_id=search_response['results'][0]["id"]
        return search_response.json()
    
    
    def create_page(self, data: dict):
        create_url = "https://api.notion.com/v1/pages"

        #payload = {"parent": {"database_id": DATABASE_ID}, "properties": data}

        res = requests.post(create_url, headers=self.notion_headers, json=data)
        print(res.text)
        return res

    def query_database(self, num_pages = None):
        """
        If num_pages is None, get all pages, otherwise just the defined number.
        """
        url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"

        get_all = num_pages is None
        page_size = 100 if get_all else num_pages

        payload = {"page_size": page_size}
        response = requests.post(url, json=payload, headers=self.notion_headers)

        data = response.json()

        #Comment this out to dump all data to a file
        import json
        with open('db.json', 'w', encoding='utf8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        results = data["results"]
        # while data["has_more"] and get_all:
        #     payload = {"page_size": page_size, "start_cursor": data["next_cursor"]}
        #     url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
        #     response = requests.post(url, json=payload, headers=self.notion_headers)
        #     data = response.json()
        #     results.extend(data["results"])

        return data


#answer = DatabaseConnection(SECRET_KEY,HEADERS, DATABASE_ID).response_search()

payload = {
    "parent": {
        "database_id": DATABASE_ID
    },
    "properties": {
                "activity_type": {
                    "select": {
                        "name": "Listening",
                    }
                },
                "Description": {
                    "id": "title",
                    "type": "title",
                    "title": [
                        {
                            "type": "text",
                            "text": {
                                "content": "Fait test"}
                        }]
}}}

#read_db =  DatabaseConnection(SECRET_KEY,HEADERS,DATABASE_ID).query_database()
create_test = DatabaseConnection(SECRET_KEY,HEADERS,DATABASE_ID).create_page(payload)
print(create_test)