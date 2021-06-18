from django.core.management.base import BaseCommand, CommandError
from app.models import *
from datetime import date
import random, string
from random import choice

def makeTitle(str):
    letters = ''
    for i in range(len(str)-2):
        letters += random.choice(string.ascii_lowercase) 
    new_str = str[0] + letters + str[-1]
    return new_str

def makeText(length):
    letters = ''
    for i in range(length):
        letters += random.choice(string.ascii_lowercase) 
    return letters   

class Command(BaseCommand):

    def handle(self, *args, **options):
        base = 4
        amount_users = base
        amount_questions = base*10
        amount_tags = base
        amount_answers = base*100
        amount_likes = base*200

        # теги
        for i in range(amount_tags):
            nt = Tag(word = makeTitle('tag')+f'_{(i*7+29)%89+10}')
            self.stdout.write(nt.word)
            nt.save()
            print("saved")

        # авторы
        # usernames = set(list(User.objects.values_list('username', flat=True)))
        for i in range(amount_users):
            username_=makeTitle('Author')+f'_{(i*7+29)%89+10}'
            # bool flag = true
            # while(flag)
            #     flag = false
            #     for j in usernames:
            #         if (j == username_)
            #             flag = true
            #     if(flag)
            #         username_=makeTitle('Author')+f'_{(i*7+29)%89+10}'
            
            us = User(username = username_ , email=f'{username_}@mail.ru', password=makeTitle('password'))
            author = Author(user = us)
            us.save()
            author.save()

        fact_amount_users = Author.objects.count()
        print(fact_amount_users)

        # вопросы
        author_ids = list(
            Author.objects.values_list(
                'id', flat=True
            )
        )
        tag_ids = list(
            Tag.objects.values_list(
                'id', flat=True
            )
        )
        answer_ids = list(
            Answer.objects.values_list(
                'id', flat=True
            )
        )
        for i in range(amount_questions):
            start_date = date.today().replace(day=1, month=1).toordinal()
            end_date = date.today().toordinal()
            random_day = date.fromordinal(random.randint(start_date, end_date))
            q = Question(title=makeTitle('Question')+f'_{(i*7+29)%89+7}', text=makeText(i*242%147+88), pub_date=random_day)
            q.author = choice(author_ids)
            q.save() 
            print("q saved")
            # rating = min( 5+(i%5), fact_amount_users)
            # d = []
            # for j in range (rating):
            #     d.append(Author.objects.get(id=j%fact_amount_users+1))
            # q.likers.set(d)
            fact_amount_tags = Tag.objects.count()
            amount_of_tags_q = min( 7+(i%5), fact_amount_tags )
            t = []
            # print("q rating ok")
            for j in range (amount_of_tags_q):
                t.append( Tag.get(id = choice(tag_ids)) )
                print("j in tags: ", j)
            q.tags.set(t)
            q.save()

        # ответы
        for i in range(amount_answers):
            ans = Answer(author = Author.objects.get(id=j%fact_amount_users+1), text = makeText(i*42%17+79))
            ans.save()