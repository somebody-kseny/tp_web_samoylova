1. python3 -m venv venv
2. python3 manage.py migrate
3. python3 manage.py fill_base 5
Скрипт принимает значение (равное количестову пользователей и тегов), относительно которого рассчитывает остальные:
amount_users = base
amount_questions = base*10
amount_tags = base
amount_answers = base*100
amount_likes = base*200
4. python3 manage.py runserver
Для входа на сайте при желании можно использовать пользователя Vinni, пароль honey
Для входа в админку нужно руками createsuperuser

