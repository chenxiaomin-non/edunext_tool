import requests
import get_course
import get_lesson
import edu_header
import get_question
import get_comment


def test_connection():
    print('\n\t--- EduNext Tools for Lazier ---\n')

    headers = edu_header.headers
    token = edu_header.get_token()
    headers['authorization'] = token

    if len(token.strip()) == 0:
        print('No token found!\nInsert your token into .token file!')
        return

    resp = requests.get(
        url='https://fuapi.edunext.vn/learn/v2/classes/get-course-current-of-user', headers=headers)
    if resp.status_code != 200:
        print(
            "Connection to Edunext failed!\nPlease check your Internet and try again later!")
        return

    for k, v in edu_header.user_information.items():
        print('\t', k, ':', v)

    print('\t---------------------------------\n\tOK to connect to Edunext!\n\t---------------------------------\n')


def auto_vote_sao(course: dict):
    print('\t--- Vote Sao For Subject', course['externalcode'], '---\n')
    lesson, classId, courseId = get_lesson.get_lesson(
        course['classId'], course['id'])

    index = 1
    for l in lesson:
        print('Lesson: ', index)
        index += 1
        session_id, active_question = get_lesson.get_active_question(l)
        for question in active_question:
            print('\t -', str(question['description']
                              ).replace('<p>', '').replace('</p>', ''))
            get_question.vote_sao(
                question['id'], classId, question['title'], session_id)


def auto_answer_question(course: dict):
    print('\t--- Answer Question Of Course', course['externalcode'], '---\n')
    lesson, classId, courseId = get_lesson.get_lesson(
        course['classId'], course['id'])

    index = 1
    for l in lesson:
        print('Lesson: ', index)
        index += 1
        session_id, active_question = get_lesson.get_active_question(l)
        for question in active_question:
            groupid = get_question.get_question_info(question['id'], session_id)
            print('\t -', str(question['description']
                              ).replace('<p>', '').replace('</p>', ''))
            get_comment.get_comment_of_question(
                question['id'], groupid, session_id)


def auto_vote_comment(course: dict):
    print('\t--- Answer Question Of Course', course['externalcode'], '---\n')
    lesson, classId, courseId = get_lesson.get_lesson(
        course['classId'], course['id'])

    index = 1
    for l in lesson:
        print('Lesson: ', index)
        index += 1
        session_id, active_question = get_lesson.get_active_question(l)
        for question in active_question:
            groupid = get_question.get_question_info(question['id'], session_id)
            print('\t -', str(question['description']
                              ).replace('<p>', '').replace('</p>', ''))
            


# running part
if __name__ == "__main__":
    test_connection()

    list_course = get_course.get_course()
    
    while True:
        get_course.process_course(list_course)
        try:
            choice = int(input("Index of your course: ")) - 1
        except Exception:
            continue
        # select course
        selected_course = list_course[choice]
        # end select course

        # vote sao
        auto_vote_sao(selected_course)

        # auto comment
        auto_answer_question(selected_course)

        # auto vote comment

