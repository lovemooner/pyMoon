import json
import requests

# GET /frcIssues  
base_url1 = "https://fuscdrmsmc268-fa-ext.us.oracle.com/fscmRestApi/resources/latest/frcIssues"
usr = "FRC_WSUSER"
pwd = "Welcome1"

resp1 = requests.get(base_url1, auth=(usr, pwd))
print('GET request ', base_url1, resp1.status_code)

if resp1.status_code != 200:
    # This means something went wrong.
    print('** GET error ', resp1.status_code)
    quit()

data1 = resp1.json()
print(data1)

# GET /frcIssues/{issueId}
issueId = data1['items'][0]['IssueId']

base_url2 = base_url1 + "/" + str(issueId)
resp2 = requests.get(base_url2, auth=(usr, pwd))

if resp2.status_code != 200:
    # This means something went wrong.
    print('** GET error ', resp2.status_code)
    quit()
    
print('GET item request ', base_url2, resp2.status_code)

data2 = resp2.json()
print(data2)

