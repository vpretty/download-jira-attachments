import requests
import base64
import json
import jira
import os

#INSERT GLOBAL VARIABLES HERE
user = ''
apikey = ''
base_url = r''
base_dir = r''
jql = 'assignee=currentuser()'
limit = 100

def getJiraTickets(user,apikey,base_url,base_dir,jql,limit):
    #Authentication
    base64_user_pass = base64.b64encode(f"{user}:{apikey}".encode()).decode()
    search_url = base_url+'//'+r'rest/api/3/search'
    offset = 0
    
    headers = {
        "Authorization": f"Basic {base64_user_pass}",
        "Accept": "application/json"
        }
    id_list = []
    id_dict = {}
    has_next_page = True


    while has_next_page == True:
        query = {
            "expand": "renderedFields",
            "maxResults": limit,
            "startAt": offset,
            "jql": jql
            }
        
        response = requests.get(search_url, headers=headers, params=query)
        data = response.json()

        if not data['issues']:
            has_next_page = False
        else:
            for issue in data['issues']:
                id_list.append(issue['id'])
                id_dict.update({issue['id']:issue['key']})
                #print(issue['key'])

        offset += limit

    print('Issues pulled')
    #create folders

    #issue API endpoint -- download attachments
    issue_url = base_url + "//" + r"rest/api/3/issue/{id}"

    for issue_id in id_list:
        new_dir = base_dir+ "\\" + id_dict[issue_id]
        #print(new_dir)
        #print(os.path.exists(new_dir))
        if os.path.exists(new_dir) == False:
            os.mkdir(new_dir)
            print('New folder made at: ' + new_dir)
        else:
            print(id_dict[issue_id] + ' already exists.')
            continue
        
        response = requests.get(issue_url.format(id=issue_id),headers=headers)
        #print(response.encoding)
        #print('Status: ' + str(response.status_code))
        issue_data = response.json()

        if 'fields' in issue_data and 'attachment' in issue_data['fields']:
            for attachment in issue_data['fields']['attachment']:
                if attachment['filename'] != []:
                    fileName = attachment['filename']
                    filePath = new_dir + "\\" + fileName
                    r = requests.get(attachment['content'],headers=headers,stream=True)
                    try:
                        with open(filePath, "wb") as f:
                            f.write(r.content)
                        f.close()
                    except:
                        print('Error: File not saved.')
                    else:
                        print(id_dict[issue_id] + ': ' + fileName + ' saved.')
                else:
                    print('no attachment content')
        else:
            print("fields not in json")
    

def main(user,apikey,base_url,base_dir,jql,limit):
    getJiraTickets(user,apikey,base_url,base_dir,jql,limit)

if __name__ == '__main__':
    main(user,apikey,base_url,base_dir,jql,limit)
