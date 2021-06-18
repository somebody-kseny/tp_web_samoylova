from django.contrib import admin
from app.models import Question
from app.models import Author
from app.models import Answer
from app.models import Tag

# Register your models here.
admin.site.register(Author)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Tag)
