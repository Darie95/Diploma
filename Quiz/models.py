from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

class Quiz(models.Model):
    class Meta:
        verbose_name = "Квиз"
        verbose_name_plural = "Квизы"

    def __str__(self):
        return '[{}| Quiz {}]'.format(self.id, self.name)

    name = models.CharField(max_length=250, verbose_name="Имя")
    site = models.CharField(max_length=250, null=True, verbose_name="Веб-сайт")
    description = models.TextField(null=True, verbose_name="Описание")
    category = models.CharField(max_length=250, null=True, verbose_name="Категория")
    next_game = models.DateField(null=True,verbose_name="Дата следующей игры")
    label = models.ImageField(upload_to='items/', verbose_name='Изображение',
                              null=True, blank=True)

class Positions(models.Model):
    class Meta:
        verbose_name = "Критерий"
        verbose_name_plural = "Критерии"

    def __str__(self):
        return '[{}| Quiz {}]'.format(self.id, self.name)


    name = models.CharField(max_length=250, verbose_name="Название критерия")
    share = models.IntegerField(verbose_name="Удельный вес")

class Values(models.Model):
    class Meta:
        verbose_name = "Оценка"
        verbose_name_plural = "Оценки"

    def __str__(self):
        return '[{}| Quiz {}]'.format(self.id, self.position)

    position = models.ForeignKey(Positions, related_name='criteria',
                  on_delete=models.CASCADE, verbose_name="Критерии")
    mark = models.IntegerField(verbose_name="Оценка")
    quiz = models.ForeignKey(Quiz, related_name='quizzes',
                  on_delete=models.CASCADE, verbose_name="Квизы")

class Comments(models.Model):
    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    comments_text = models.TextField(verbose_name="Текст комментария")
    quizz_com =  models.ForeignKey(Quiz, related_name='comm',on_delete=models.CASCADE, verbose_name="Квизы")
    author_com =  models.CharField(max_length=250, verbose_name="Автор")
    comments_date = models.DateTimeField(default=datetime.now(),verbose_name="Дата комментария" )


class DatesPlaces(models.Model):
    for_quiz = models.ForeignKey(Quiz, related_name='dates',
                             on_delete=models.CASCADE, verbose_name="Квизы")
    game_date =  models.DateField(null=True,verbose_name="Дата игры")
    game_place =  models.CharField(max_length=250, verbose_name="Автор")
    game_date_registration = models.DateField(null=True,verbose_name="Дата регистрации")
