import time
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.fields import ContentType
from django.db import models
from django.contrib.auth.models import User
import time
from django.db.models import Count
from django.utils import timezone


# from app.forms import *

# Create your models here.

LIKE = True
DISLIKE = False

class AuthorManager(models.Manager):
    def calc_rating(self):
        return self.annotate()
    def get_best(self):
        return Author.objects.order_by('?')[:7]

class Author(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(upload_to='avatars/%Y/%m/%d', default='avatars/def.jpg')
    rating = models.IntegerField(default=0)

    class Meta:
        verbose_name = "Автор"
        verbose_name_plural = "Авторы"

    def __str__(self):
        return self.user.username

    objects = AuthorManager()

class QuestionManager(models.Manager):
    def calc_best(self):
        return Question.objects.order_by('rating')
    def calc_new(self):
        return Question.objects.order_by('id').reverse()

class Question(models.Model):
    id = models.AutoField(primary_key=True)
    author=models.ForeignKey(Author, on_delete=models.CASCADE)
    title = models.CharField(max_length=128)
    text = models.TextField()
    pub_date = models.DateTimeField( default=timezone.now )

    likers=models.ManyToManyField(Author, related_name='liked_questions')
    dislikers=models.ManyToManyField(Author, related_name='disliked_questions')
    rating = models.IntegerField(default=0, db_index=True)

    tags = models.ManyToManyField(
        'Tag',  related_name='questions',
        related_query_name='question'
    )
    answers = models.ManyToManyField(
        'Answer',  related_name='question',
        related_query_name='question'
    )

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

    def __str__(self):
        return self.title
    
    objects = QuestionManager()

class Answer(models.Model):
    author = models.ForeignKey('Author',default=1, on_delete=models.CASCADE)
    is_right = models.BooleanField(default=False)
    text = models.TextField()
    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"
    def __str__(self):
        return self.text

class TagManager(models.Manager):
    def best_tags(self):
        return Tag.objects.annotate(am_of_q = Count('question')).order_by('am_of_q').reverse()[:7]
    def by_tag(self, tag_str):
        return self.filter(word=tag_str).first().questions.all().order_by('pub_date').reverse()


class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    word = models.SlugField(max_length=18, allow_unicode=True)
    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
    def __str__(self):
        return self.word
    
    objects = TagManager()
