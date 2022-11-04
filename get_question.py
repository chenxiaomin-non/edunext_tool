import requests
import edu_header

json_data = []

def get_question_info(activityId: str, sessionId: str):
    headers = edu_header.headers
    params = {
        'sessionId': sessionId,
        'activityId': activityId
    }

    params['groupId'] = requests.get(
        url='https://fuapi.edunext.vn/learn/v2/course/get-session-activity-detail',
        params=params,
        headers=headers
    ).json()['data']['groupId']
    if len(edu_header.group_mate) == 0:
        
        resp = requests.get(
            url='https://fuapi.edunext.vn/learn/v2/classes/presentcritical/get-evaluate-inside-group-score', 
            params=params, headers=headers
        ).json()['data']
        edu_header.group_mate = resp

        for mate in edu_header.group_mate:
            edu_header.group_mate_dict[mate['userId']] = mate['fullName']
    return params['groupId']


def vote_sao(activityId: str, classId: str, question: str, sessionId: str):
    global json_data
    headers = edu_header.headers
    headers['content-type'] = 'application/json'

    groupid = get_question_info(activityId, sessionId)
    params = {
        'activityId': activityId,
        'classId': classId,
        'groupid': groupid,
    }
    if len(json_data) == 0:
        for p in edu_header.group_mate:
            json_data.append({
                'userId': p['userId'],
                'hardWorkingPoint': 5,
                'goodPoint': 5,
                'cooperativePoint': 5,
        })

    response = requests.post('https://fuapi.edunext.vn/learn/v2/classes/presentcritical/evaluate-inside-group', params=params, headers=headers, json=json_data).json()
    if response['code'] == 200 and response['data'] == True:
        print('\t\t-  Success Vote for Question', question)
    else:
        print('\t\t-  Fail to vote for', question)
