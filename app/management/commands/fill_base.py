from django.core.management.base import BaseCommand, CommandError
from app.models import *
from datetime import date
from django.utils.timezone import make_aware
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
        letters += ' '
        letters += random.choice(string.ascii_lowercase + ' ') 
    return letters   

class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('base', nargs='+', type=int, help="waits a number which will be use as base (amount of users), other params are calculated using recomendations")

    def handle(self, *args, **options):
        base = options['base'][0]
        amount_users = base
        amount_questions = base*10
        amount_tags = base
        amount_answers = base*100
        amount_likes = base*200

        print("plese wait, filling db...")

        # теги (таким образом могут получиться теги, для которых нет вопросов, что конечно нехорошо. зато они будут повторяться у вопросов)
        for i in range(amount_tags):
            nt = Tag(word = makeTitle('tag')+f'_{(i*7+29)%89+10}')
            nt.save()

        # автор Vinni пароль honey
        existing_usernames = set(list(User.objects.values_list('username', flat=True)))
        us = User.objects.create_user(username = 'Vinni' , email='forest@mail.ru', password='honey')
        author = Author(user = us)
        us.save()
        author.save()    

        # еще авторы
        for i in range(amount_users-1):
            username_=makeTitle('Author')+f'_{(i*7+29)%89+10}'
            while username_ in existing_usernames:
                username_=makeTitle('Author')+f'_{(i*7+29)%89+10}'
            existing_usernames.add(username_)
            us = User.objects.create_user(username = username_ , email=f'{username_}@mail.ru', password='password')
            author = Author(user = us)
            us.save()
            author.save()

        fact_amount_users = Author.objects.count()

        #
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

        # вопросы
        for i in range(amount_questions):
            print("plese wait, filling db...: new question created [", i, "\t]")

            start_date = date.today().replace(day=1, month=1).toordinal()
            end_date = date.today().toordinal()
            random_day = date.fromordinal(random.randint(start_date, end_date))
            q = Question(title=makeTitle('Question')+f'_{(i*7+29)%89+7}', text=makeText(i*242%147+88), pub_date=random_day)
            q.author = Author.objects.get(id = choice(author_ids))
            q.save()

            # теги к вопросу
            fact_amount_tags = Tag.objects.count()
            amount_of_tags_q = min( 3+(i%5), fact_amount_tags )
            t = []
            for j in range (amount_of_tags_q):
                t.append( Tag.objects.get(id = choice(tag_ids)) )
            q.tags.set(t)

            # ответы
            amount_of_answers_q = 13+(i%5)
            a = []
            for i in range(amount_of_answers_q):
                ans = Answer(author = Author.objects.get(id = choice(author_ids)), text = makeText(i*42%17+342))
                ans.save()
                a.append(ans)
            q.answers.set(a)

            # лайки
            rand = random.randint(1,amount_likes//amount_questions)
            for i in range (rand):
                q.likers.add(Author.objects.get(id = choice(author_ids)))
                q.rating += 1
            rand_second = amount_likes//amount_questions +1 -rand
            for i in range (rand_second):
                q.dislikers.add(Author.objects.get(id = choice(author_ids)))
                q.rating -= 1
            q.save()

