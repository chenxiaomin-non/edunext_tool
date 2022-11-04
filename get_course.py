import edu_header
import requests

def get_course():
    headers = edu_header.headers

    response = requests.get('https://fuapi.edunext.vn/learn/v2/classes/get-course-current-of-user', headers=headers)
    if response.status_code != 200:
        return None
    
    response = response.json()
    if response['success'] != True:
        return None
    
    data = response['data']['listCourseOfUser']

    return data

def process_course(courses: list):
    print('\n\t -------------------------------')
    print('\n\t All Course in Your EduNext')
    print('\n\t -------------------------------')
    index = 1
    for c in courses:
        print('\t', index, '-',c['externalcode'], '-', c['id'], '-', c['classId'])
        index += 1
    print('\t -------------------------------\n')
    

