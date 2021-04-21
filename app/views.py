from django.shortcuts import render
from django.core.paginator import Paginator

def get_shown_text(str):
    if len(str) < 120:
        return str
    else:
        tmp = str[120:150]
        part = tmp.split()
        return str[0:120] + part[0] + '...'

std_str = ' Vim  is a text editor.  It can be used to edit all kinds of plain text.  It is especially useful multi level undo, multi windows and buffers, syntax highlighting, command line  editing,  filenamecompletion,   on-line   help,   visual  selection,  etc..   See  ":helpvi_diff.txt for a summary of the differences between Vim and Vi. While running Vim a lot of help can be obtained from the  on-line  helpsystem, with the ":help" command.  See the ON-LINE HELP section below. Most often Vim is started to edit a single file with the command'

questions = [
    {
        'id': idx,
        'title': f'Title number {idx} long name for question long',
        'text': f'Some text for question #{idx}' + std_str,
        'shown_text': get_shown_text(f'Some text for question #{idx}' + std_str),
        'likes': idx+3,
        'user_id': idx%4,
        'user': f'user_num_{idx%4}',
        'answers': [idx, idx*2, idx*3, idx*4],
        'tags': [f'tag{idx%7}', 'tag7', f'tag{idx%7}',],
    } for idx in range(40)
]

answers = [
    {
        'id': idx,
        'text': f'Some text for answer #{idx}' + std_str,
        'likes': idx%5+3,
        'user_id': idx%7,
        'user': f'user_num_{idx%7}',
        'is_correct': False,
    } for idx in range(120)
]

tags = [
    {
        'id': idx,
        'name': f'tag{idx}',
        'questions_id': [idx, idx+2, 5],
    } for idx in range(8)
]
best_tags = tags[0:3]

users = [
    {
        'id': idx,
        'email': 'mail@yandex.ru',
        'name': f'User number {idx}',
        'avatar': f'avatar{idx}',
        'questions_id': [(idx*2)%10, (idx*3)%10, idx ],
    } for idx in range(6)
]
best_users = users[0:3]

def paginate(objects_list, request, per_page=10):
    p = Paginator(objects_list, per_page)
    page = request.GET.get('page')
    return p.get_page(page)

def typical_response(cards, request):
    return {
    'this_user': users[4],
    'cards': paginate(cards, request),
    'best_tags': best_tags,
    'best_users': best_users,
    }

# Create your views here.

def index(request):
    return render(request, 'index.html', typical_response(questions, request))

def hot_questions(request):
    return render(request, 'hot_questions.html', typical_response(questions, request))

def one_question(request, pk):
    response = typical_response(answers, request)
    response.update({ 'question': questions[pk] })
    return render(request, 'question.html', response)

def tag_page(request, name_of_tag):
    for tag in tags:
        if (tag['name'] == name_of_tag):
            questions_tag = []
            for id in tag['questions_id']:
                questions_tag.append(questions[id])
            response = typical_response(questions_tag, request)
            response.update({ 'tag': tag['name'] })
            return render(request, 'tag.html', response)
    return render(request, 'tag.html', {"questions": [], "tag": "нет такого тега"})
    
def login(request):
    return render(request, 'login.html', typical_response(questions, request))

def signup(request):
    return render(request, 'signup.html', typical_response(questions, request))

def ask(request):
    return render(request, 'ask.html', typical_response(questions, request))

def settings(request):
    return render(request, 'settings.html', typical_response(questions, request))

def user_question(request, pk):
    user = users[pk]
    questions_user = []
    for id in user['questions_id']:
        questions_user.append(questions[id])
    response = typical_response(questions_user, request)
    response.update({ 'user': user })
    return render(request, 'user_question.html', response)