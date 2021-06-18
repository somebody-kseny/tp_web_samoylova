# Generated by Django 3.1.7 on 2021-06-18 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_auto_20210528_1111'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='author',
        ),
        migrations.RemoveField(
            model_name='question',
            name='likers',
        ),
        migrations.RemoveField(
            model_name='question',
            name='tegs',
        ),
        migrations.AddField(
            model_name='question',
            name='tags',
            field=models.ManyToManyField(related_name='questions', related_query_name='question', to='app.Tag'),
        ),
        migrations.CreateModel(
            name='Likes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dislikers', models.ManyToManyField(related_name='dislikers', related_query_name='disliker', to='app.Author')),
                ('likers', models.ManyToManyField(related_name='likers', related_query_name='liker', to='app.Author')),
            ],
        ),
    ]