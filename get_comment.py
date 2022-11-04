import edu_header
import requests
from random import randint
import get_lesson

def get_comment_of_question(activityId: str, groupId: str, sessionId: str, hasComment = False, commentId = None):
    headers = edu_header.headers
    params = {
        'Contextid': activityId,
        'CourseId': get_lesson.lesson_info['courseId'],
        'ParentKey': groupId,
        'isPublic': True
    }

    resp = requests.get(url='https://fuapi.edunext.vn/comment/v1/activity/get-comments', headers=headers, params=params).json()
    
    if hasComment is True:
        question_info = {
            'contextId': activityId,
            'courseId': get_lesson.lesson_info['courseId'],
            'groupId': groupId,
            'Id': commentId
        }
        delete_comment(question_info)
        print('\t\t- Comment deleted')

    comments = list()
    has_own_comment = False
    first_comment = None
    for cmt in resp['Comments']:
        if cmt['Parent'] == 0:
            comments.append(cmt)
            first_comment = cmt

            # if you answered
            if cmt['Creator'] == int(edu_header.user_information['UserId']):
                if cmt['Content'] == '<p>.</p>':
                    question_info = {
                        'contextId': activityId,
                        'courseId': get_lesson.lesson_info['courseId'],
                        'groupId': groupId,
                        'Id': cmt['Id']
                    }
                    delete_comment(question_info)
                    continue
                has_own_comment = True
                print('\t\t- You answered that:', cmt['Content'][3:25], '...')

                # get vote card and vote for un-voted comment
                cardVoted = resp['CardsVoted']
                remain_card = [
                    cardVoted[2]['RemainVote'],
                    cardVoted[0]['RemainVote'],
                    cardVoted[1]['RemainVote'],
                    cardVoted[3]['RemainVote']    
                ]
                
                max_point = 4
                for c in resp['Comments']:
                    if c['Parent'] != 0:
                        continue
                    if c['Creator'] == int(edu_header.user_information['UserId']):
                        continue
                    is_voted = False
                    for card in c['Cards']:
                        if card['IsVoted'] is True:
                            if card['CardValue'] < max_point:
                                vote_comment(c, sessionId, card['CardValue'], True)
                                print('\t\t- Unvoted for', edu_header.group_mate_dict[c['Creator']], card['CardValue'], '⭐')
                                break
                            is_voted = True
                            print('\t\t- Voted for', edu_header.group_mate_dict[c['Creator']], card['CardValue'], '⭐')
                            break
                    if is_voted is False:
                        if remain_card[max_point-1] != 0:
                            vote_comment(c, sessionId, max_point)
                            remain_card[max_point-1] -= 1
                            print('\t\t- Voted for', edu_header.group_mate_dict[c['Creator']], max_point, '⭐')
                        else:
                            max_point -= 1
                            remain_card[max_point-1] -= 1
                            vote_comment(c, sessionId, max_point)
                            print('\t\t- Voted for', edu_header.group_mate_dict[c['Creator']], max_point, '⭐')


    # if u have not answered yet
    if has_own_comment is False:       
        question_info = {
            'ActivityId': activityId, 
            'ClassId': get_lesson.lesson_info['classId'],
            'CourseId': get_lesson.lesson_info['courseId'],
            'GroupId': groupId,
            'SessionId': sessionId
        }

        if first_comment is None:
            if hasComment is True:
                print('\t\t- There is really no comment')
            print('\t\t- There is no comment here!')
            try: 
                comment = post_comment_if_have_no_comment('<p>.</p>', question_info)
                print('\t\t- Post new "." comment with id =', comment['Id'])
                get_comment_of_question(activityId, groupId, sessionId, True, comment['Id'])
            except Exception:
                print('\t\t- Stupid error occur! Or Finished Question!')
                return
            return

        if first_comment is not None:
            print('\t\t- There are %d comments' % (len(comments),))
            result = post_comment_if_have_no_comment(first_comment['Content'], question_info)
            print('\t\t- Post new comment ')


def post_comment_if_have_no_comment(content: str, question_info: dict):
    headers = edu_header.headers
    headers['content-type'] = 'application/json'
    url = 'https://fuapi.edunext.vn/comment/v1/activity/add-comment'
    payload = {
        'ActivityId': question_info['ActivityId'],
        'ClassId': question_info['ClassId'],
        'ClientKey': "add-%s-%d" % (question_info['ActivityId'], randint(1667574171022, 1667575171022)),
        'Content': content,
        'ContextId': question_info['ActivityId'],
        'CourseId': question_info['CourseId'],
        'CurrentUrl': 'https://fu.edunext.vn/en/session/activity?sessionid=%s&activityId=%s' % (question_info['SessionId'], question_info['ActivityId']),
        'GroupId': question_info['GroupId'],
        'ParentId': 0,
        'ParentIdComment': 0,
        'ParentKey': question_info['GroupId'],
        'Pings': "{}",
        "id": 0
    }
    resp = requests.post(url=url, headers=headers, json=payload).json()
    
    return resp


def delete_comment(question_info: dict):
    payload = {
        'ContextId': question_info['contextId'],
        'CourseId': question_info['courseId'],
        'CurrentGroupId': question_info['groupId'],
        'GroupId': question_info['groupId'],
        'Id': question_info['Id']
    }
    headers = edu_header.headers
    headers['content-type'] = 'application/json'
    resp = requests.post(url='https://fuapi.edunext.vn/comment/v1/del-comment', headers=headers, json=payload).text
    return resp


def vote_comment(comment: dict, sessionId: str, point: int, unvote = False):
    card_type = {
        1: 4,
        2: 3,
        3: 2,
        4: 1
    }
    type = card_type[point]
    payload = {
        'ActivityId': comment['Contextid'],
        'CardType': type,
        'ClassId': comment['ClassId'],
        'ClientKey': 'vote-%s-%d' % (comment['Id'], randint(1667590831520, 1667590931520)),
        'CommentId': comment['Id'],
        'CourseId': get_lesson.lesson_info['courseId'],
        'CurrentGroupId': comment['GroupId'],
        'CurrentUrl': 'https://fu.edunext.vn/en/session/activity?sessionid=%s&activityId=%s' % (sessionId, comment['Contextid']),
        'GroupId': comment['GroupId'],
        'IsVoted': unvote,
        'OnwId': comment['Creator']
    }
    headers = edu_header.headers
    headers['content-type'] = 'application/json'
    resp = requests.post(url='https://fuapi.edunext.vn/comment/v1/save-voted-card', headers=headers, json=payload)

    if resp.json().get('Errors', None) != None:
        vote_comment(comment, sessionId, point-1)

def vote_for_comment_if_not_vote_yet():
    pass