import requests
import json
import logging
import sched, time
import socket


HOST = '0.0.0.0'
PORT = 7265


def new_events():
    logging.basicConfig(level=logging.INFO, filename='conflue_audit.log', format='%(asctime)s %(levelname)s:%(message)s')
    list_events = []
    try:
        headers = {
                'Authorization': 'Basic <API_key>',
                'Content-Type': 'application/json',
                      }
        response = requests.get('https://confluence_address/rest/api/audit/?limit=1000', headers=headers)
        text0 = json.loads(response.text)
        # print(text0)
        for k in text0['results']:
            # print(k)
            list_data = []
            with open("conflue_audit.log", 'r') as f:
                data = f.read()
                if str(k["creationDate"]) in data:
                    continue
                else:
                    logging.basicConfig(level=logging.INFO, filename='conflue_audit2.log',
                                        format='%(asctime)s %(levelname)s:%(message)s')
                    if 'author' in k:
                        if k['author']['username'] == '' and k['author']['userKey'] == '':
                            author = ["author_type", k['author']['type'], "author_Displ_name",
                                      k['author']['displayName'],
                                      "author_username", "None", "author_key", "None"]
                            list_data.extend(author)
                        else:
                            author = ["author_type",k['author']['type'],"author_Displ_name",k['author']['displayName'],
                                  "author_username",k['author']['username'],"author_key", k['author']['userKey']]
                            list_data.extend(author)
                    else:
                        author = ["author", 'None']
                        list_data.extend(author)
                    if 'remoteAddress' in k:
                        if k['remoteAddress'] == '':
                            remote = ["remoteAddress", 'None']
                            list_data.extend(remote)
                        else:
                            remote = ["remoteAddress", k['remoteAddress']]
                            list_data.extend(remote)
                    else:
                        remote = ["remoteAddress", 'None']
                        list_data.extend(remote)
                    if 'creationDate' in k:
                        created = ["creationDate", str(k['creationDate'])]
                        list_data.extend(created)
                    else:
                        created = ["creationDate", 'None']
                        list_data.extend(created)
                    if 'summary' in k:
                        summary = ["name_event", k['summary']]
                        list_data.extend(summary)
                    else:
                        summary = ["name_event", 'None']
                        list_data.extend(summary)
                    if 'description' in k:
                        if k['description'] == '':
                            description = ["description", 'None']
                            list_data.extend(description)
                        else:
                            description = ["description", k['description']]
                            list_data.extend(description)
                    else:
                        description = ["description", 'None']
                        list_data.extend(description)
                    if 'category' in k:
                        if k['category'] == '':
                            category = ["category", 'None']
                            list_data.extend(category)
                        else:
                            category = ["category", k['category']]
                            list_data.extend(category)
                    else:
                        category = ["category", 'None']
                        list_data.extend(category)
                    if 'sysAdmin' in k:
                        if k['sysAdmin'] == '':
                            sysAdmin = ["sysAdmin", 'None']
                            list_data.extend(sysAdmin)
                        else:
                            sysAdmin = ["sysAdmin", k['sysAdmin']]
                            list_data.extend(sysAdmin)
                    else:
                        sysAdmin = ["sysAdmin", 'None']
                        list_data.extend(sysAdmin)
                    if 'affectedObject' in k:
                        affectedObject = ["affectedObject", "name", k['affectedObject']['name'],
                                          "objectType", k['affectedObject']['objectType']]
                        list_data.extend(affectedObject)
                    else:
                        affectedObject = ["affectedObject", 'None']
                        list_data.extend(affectedObject)
                    if k['changedValues'] == []:
                        changedValues = ["changedValues", 'None']
                        list_data.extend(changedValues)
                    else:
                        for kk in k['changedValues']:
                            changedValues = ["changedValues", "name", kk['name'],
                                             "oldValue", kk['oldValue'], "newValue", kk['newValue']]
                        list_data.extend(changedValues)
                    if k['associatedObjects'] == []:
                        associatedObjects = ["associatedObjects", 'None']
                        list_data.extend(associatedObjects)
                    else:
                        for kk in k['associatedObjects']:
                            associatedObjects = ["associatedObjects", "name", kk['name'],
                                          "objectType", kk['objectType']]
                        list_data.extend(associatedObjects)
                    logging.info(list_data)
            list_events.append(list_data)
    except OSError as e:
        logging.error("error reading the file")

    with open('conflue_audit.log', 'r') as file:
        data3 = file.read()
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(data3.encode())


new_events()
