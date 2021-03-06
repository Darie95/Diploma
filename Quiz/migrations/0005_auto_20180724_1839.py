# Generated by Django 2.0.7 on 2018-07-24 16:39

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Quiz', '0004_auto_20180723_2022'),
    ]

    operations = [
        migrations.CreateModel(
            name='Positions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=250, verbose_name='Название критерия')),
                ('share', models.IntegerField(verbose_name='Удельный вес')),
            ],
            options={
                'verbose_name': 'Критерий',
                'verbose_name_plural': 'Критерии',
            },
        ),
        migrations.CreateModel(
            name='Values',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mark', models.IntegerField(verbose_name='Оценка')),
                ('position', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='criteria', to='Quiz.Positions', verbose_name='Критерии')),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='quizzes', to='Quiz.Quiz', verbose_name='Квизы')),
            ],
            options={
                'verbose_name': 'Оценка',
                'verbose_name_plural': 'Оценки',
            },
        ),
        migrations.RemoveField(
            model_name='criteria',
            name='quiz',
        ),
        migrations.AlterField(
            model_name='comments',
            name='comments_date',
            field=models.DateTimeField(default=datetime.datetime(2018, 7, 24, 18, 39, 27, 692411), verbose_name='Дата комментария'),
        ),
        migrations.DeleteModel(
            name='Criteria',
        ),
    ]
