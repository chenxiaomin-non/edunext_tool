import edu_header
import requests

lesson_info = {}

def get_lesson(classId: str, courseId: str):
    params = {
        'classId': classId,
        'courseId': courseId
    }

    headers = edu_header.headers

    response = requests.get('https://fuapi.edunext.vn/learn/v2/classes/get-class-sessions-details', params=params, headers=headers)
    if response.status_code != 200:
        return None
    
    response = response.json()
    if response['success'] != True:
        return None
    
    data = response['data']['sessions']

    global lesson_info
    lesson_info = {
        'classId': classId,
        'courseId': courseId
    }
    return data, classId, courseId

def get_active_question(session: dict):
    session_id = session['sessionId']
    questions = session['sections'][0]['activities']
    active_questions = list()
    for q in questions:
        if q['startTime'] != "0001-01-01T00:00:00":
            active_questions.append(q)
    
    return session_id, active_questions