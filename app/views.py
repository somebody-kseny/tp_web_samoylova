from django.shortcuts import render

def get_shown_text(str):
    if len(str) < 10:
        return str
    else:
        part = str[10:40].split(' ,.;!?', maxsplit=1)
        return str[0:10] + part[0] + '...'

std_str = ' Vim  is a text editor that is upwards compatible to Vi.  It can be used to edit all kinds of plain text.  It is especially useful multi level undo, multi win‐ dows and buffers, syntax highlighting, command line  editing,  filenamecompletion,   on-line   help,   visual  selection,  etc..   See  ":helpvi_diff.txt for a summary of the differences between Vim and Vi. While running Vim a lot of help can be obtained from the  on-line  helpsystem, with the ":help" command.  See the ON-LINE HELP section below. Most often Vim is started to edit a single file with the command'

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
    } for idx in range(10)
]

answers = [
    {
        'id': idx,
        'text': f'Some text for answer #{idx}' + std_str,
        'likes': idx%5+3,
        'user_id': idx%7,
        'user': f'user_num_{idx%7}',
        'is_correct': False,
    } for idx in range(40)
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
        'name': f'User number {idx}',
        'avatar': f'avatar{idx}',
        'questions_id': [(idx*2)%10, (idx*3)%10, idx ],
    } for idx in range(6)
]

best_users = users[0:3]

def answer_amount(pk):
    return len(questions[pk].answers)

# Create your views here.

def index(request):
    return render(request, 'index.html', {'questions': questions, 'best_tags': best_tags, 'best_users': best_users})


def hot_questions(request):
    return render(request, 'hot_questions.html', {'questions': questions, 'best_tags': best_tags, 'best_users': best_users})

def one_question(request, pk):
    question = questions[pk]
    return render(request, 'question.html', {'question': question, 'best_tags': best_tags, 'best_users': best_users, 'answers': answers})

def tag_page(request, name_of_tag):
    for tag in tags:
        if (tag['name'] == name_of_tag):
            questions_tag = []
            for id in tag['questions_id']:
                questions_tag.append(questions[id])
            return render(request, 'tag.html', {"questions": questions_tag, "tag": tag['name'], 'best_tags': best_tags,'best_users': best_users })
    return render(request, 'tag.html', {"questions": [], "tag": "нет такого тега"})
    
def login(request):
    return render(request, 'login.html', {'best_tags': best_tags, 'best_users': best_users})

def signup(request):
    return render(request, 'signup.html', {'best_tags': best_tags, 'best_users': best_users})

def ask(request):
    return render(request, 'ask.html', {'best_tags': best_tags, 'best_users': best_users})

def settings(request):
    return render(request, 'settings.html', {'best_tags': best_tags, 'best_users': best_users})

def user_question(request, pk):
    user = users[pk]
    questions_user = []
    for id in user['questions_id']:
        questions_user.append(questions[id])
    return render(request, 'user_question.html', {'best_tags': best_tags, 'best_users': best_users, 'user': user, 'questions':questions_user})