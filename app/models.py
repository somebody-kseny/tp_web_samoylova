import time
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.fields import ContentType
from django.db import models
from django.contrib.auth.models import User
import time

# Create your models here.

class AuthorManager(models.Manager):
    def calc_rating(self):
        return self.annotate()

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
        return Question.objects.order_by(rating)[:5]
    def calc_new(self):
        return Question.objects.order_by(pub_date)[:5]

class Question(models.Model):
    id = models.AutoField(primary_key=True)
    # author=models.ForeignKey('Author', on_delete=models.CASCADE)
    author_id = models.IntegerField
    title = models.CharField(default = 'titleForQuestion', max_length=128)
    text = models.TextField(default='myQuestion')
    pub_date = models.DateTimeField('date published')

    rating = models.IntegerField(default=0, db_index=True)

    tags = models.ManyToManyField(
        'Tag',  related_name='questions',
        related_query_name='question'
    )
    answers = models.ManyToManyField(
        'Answer',  related_name='questions',
        related_query_name='question'
    )

    class Meta:
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

    def __str__(self):
        return self.title
    
    objects = QuestionManager()

class Answer(models.Model):
    id = models.AutoField(primary_key=True)
    author = models.ForeignKey('Author', on_delete=models.CASCADE)
    is_right = models.BooleanField(default=False)
    text = models.TextField(default='I don\'t know, but...')
    class Meta:
        verbose_name = "Ответ"
        verbose_name_plural = "Ответы"
    def __str__(self):
        return self.text

class TagManager(models.Manager):
    def best_tags(self):
        return Tag.objects.all()[:5]
    def by_tag(self, tag_str):
        return self.filter(word=tag_str).first().question.all().order_by('pub_date').reverse()


class Tag(models.Model):
    id = models.AutoField(primary_key=True)
    word = models.SlugField(max_length=18, allow_unicode=True)
    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"
    def __str__(self):
        return self.word
    
    objects = TagManager()

class Likes(models.Model):

    likers = models.ManyToManyField(
        'Author', related_name='likers',
        related_query_name='liker'
    )
    dislikers = models.ManyToManyField(
        'Author', related_name='dislikers',
        related_query_name='disliker'
    )
