from django.shortcuts import render, redirect, reverse
from django.core.paginator import Paginator
from django.contrib.auth import authenticate
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import login as auth_login
# from django.contrib.auth import *
from django.contrib.auth.models import User
# from django.contrib.auth.models import *
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.http import Http404, HttpResponseRedirect
from .forms import LoginForm, QuestionForm, AnswerForm, AuthorForm, EditAuthorForm

from app.models import *

def get_shown_text(str):
    if len(str) < 120:
        return str
    else:
        tmp = str[120:150]
        part = tmp.split()
        return str[0:120] + part[0] + '...'

def paginate(objects_list, request, per_page=10):
    p = Paginator(objects_list, per_page)
    page = request.GET.get('page')
    return p.get_page(page)

def typical_response(cards, request):
    response = {
    'cards': paginate(cards, request),
    'best_tags': Tag.objects.best_tags(),
    'best_users': Author.objects.get_best()
    }
    return response

# Create your views here.

def index(request):
    return render(request, 'index.html', typical_response(Question.objects.calc_new(), request))

def hot_questions(request):
    return render(request, 'hot_questions.html', typical_response(Question.objects.calc_best().reverse(), request))

def one_question(request, pk):
    try:
        q = Question.objects.get(id=pk)
    except Question.DoesNotExist:
        raise Http404("Нет такого вопроса")

    if request.method == 'GET':
        form = AnswerForm()    
    else:
        form = AnswerForm(data=request.POST)
        if(form.is_valid):
            an = form.save()
            an.author = Author.objects.get(user=request.user)
            an.save()
            q.answers.add(an)
            q.save()
            return redirect('/question/' + str(q.id))    
    response = typical_response(q.answers.all(), request)
    response.update({ 'question': q })
    response.update({'form': form})
    return render(request, 'question.html', response)

def tag_page(request, name_of_tag):
    if(Tag.objects.filter(word=name_of_tag)):
        response = typical_response(Tag.objects.by_tag(name_of_tag), request)
        response.update({ 'tag': name_of_tag })
        return render(request, 'tag.html', response)
    raise Http404("Нет такого тега")


def login(request):
    if request.method == 'GET':
        form = LoginForm()    
    else:
        form = LoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                if(request.POST.get('next')) :
                    return HttpResponseRedirect(request.POST.get('next'))
                else:
                    return redirect(reverse('main_page'))
            else:
                form.add_error(None, 'Неверный логин или пароль')
                response = typical_response(Question.objects.calc_best(), request)
                response.update({'form': form})
                return render(request, 'login.html', response)
    response = typical_response(Question.objects.calc_best(), request)
    response.update({'form': form})
    return render(request, 'login.html', response)

def logout(request):
    if request.user.is_authenticated:
        auth_logout(request)
    return HttpResponseRedirect(request.GET.get('next'))

def signup(request):
    if request.user.is_authenticated:
        return redirect(reverse('logout'))
    if request.method == 'GET':
        form = AuthorForm()    
    else:
        form = AuthorForm(data=request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            ath = Author.objects.create(user=new_user)
            ath.save()
            return redirect(reverse('main_page'))
        else:
            response = typical_response(Question.objects.calc_best(), request)
            response.update({'form': form})
            return render(request, 'sign.html', response)
    response = typical_response(Question.objects.calc_best(), request)
    response.update({'form': form})  
    return render(request, 'signup.html', response)

@login_required(login_url='/login/')
def ask(request):
    if request.user.is_authenticated:
        if request.method == 'GET':
            form = QuestionForm()    
        else:
            form = QuestionForm(data=request.POST)
            if(form.is_valid):
                question = form.save(commit=False)
                question.author = Author.objects.get(user=request.user)
                question.save()
                for tag in request.POST.get('tags').split(','):
                    t_obj = Tag.objects.create(word=tag)
                    t_obj.save()
                    question.tags.add(t_obj)
                question.save()
                return redirect('/question/' + str(question.id))
        response = typical_response(Tag.objects.all()[:1], request)
        response.update({'form': form})
        return render(request, 'ask.html', response)
    else:
        return redirect(reverse('login'))

@login_required(login_url='/login/')
def profile(request):
    return render(request, 'settings.html', typical_response(Question.objects.filter(author = Author.objects.get(user=request.user)), request))

@login_required(login_url='/login/')
def edit(request):
    if request.method == 'GET':
        form = EditAuthorForm()    
    else:
        form = EditAuthorForm(data=request.POST)
        if form.is_valid():
            request.user.set_password(form.cleaned_data['password'])
            request.user.save()
            return redirect(reverse('profile'))
        else:
            response = typical_response(Question.objects.calc_best(), request)
            response.update({'form': form})
            return render(request, 'edit.html', response)
    response = typical_response(Question.objects.calc_best(), request)
    response.update({'form': form})  
    return render(request, 'edit.html', response)

def user_question(request, pk):
    response = typical_response(Question.objects.filter(author = Author.objects.get(id=pk)), request)
    response.update({ 'user': Author.objects.get(id=pk) })
    return render(request, 'user_question.html', response)