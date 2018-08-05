from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.db.models import Min, Max, Avg, Count, Sum

from Quiz.forms import UserCreationForm, SearchForm, FilterForm
from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect
from django.views.generic.base import View
from Quiz.models import Quiz, Comments, Positions, Values, DatesPlaces, Point, \
    AnketaDone, Anketa, Participants
from django.db.models import Q
from Quiz.forms import CommentForm
from django.contrib.auth.models import User
from datetime import datetime
import matplotlib as mpl

mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
import csv
import os


def main(request):
    return render(request, 'main.html')


class Search(FormView):
    template_name = 'search.html'
    form_class = SearchForm

    def form_valid(self, form):
        data = form.cleaned_data
        result = Quiz.objects.filter((Q(name__icontains=data['search']) | (
            Q(category__icontains=data['search']))))
        return render(self.request, 'search_result.html', {'items': result})


class RegisterFormView(FormView):
    form_class = UserCreationForm
    success_url = "/"
    template_name = "register.html"

    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)


class LoginFormView(FormView):
    form_class = AuthenticationForm
    success_url = "/"
    template_name = "login.html"

    def form_valid(self, form):
        self.user = form.get_user()
        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)

        return HttpResponseRedirect("/")


def about_quiz(request):
    quiz_all = Quiz.objects.all()
    return render(request, 'about_quiz.html', {'quiz_all': quiz_all})


class Details(View):
    def get(self, request, quiz_id):
        try:
            context = {'quiz': Quiz.objects.get(id=quiz_id),
                       'comments': Comments.objects.all().filter(
                           quizz_com=Quiz.objects.get(id=quiz_id)),
                       'form_comments': CommentForm}
        except Quiz.DoesNotExist:
            return redirect('index')
        return render(self.request, 'details.html', context)

    def post(self, request, quiz_id):
        form = CommentForm
        new = Quiz.objects.get(id=quiz_id)
        if form.is_valid and request.user.is_authenticated:
            Comments.objects.create(
                comments_text=request.POST.get("comments_text"),
                quizz_com=new, author_com=User.objects.get(id=request.user.id)
            )
            context_1 = {'quiz': Quiz.objects.get(id=quiz_id),
                         'comments': Comments.objects.all().filter(
                             quizz_com=Quiz.objects.get(id=quiz_id)),
                         'warning': '',
                         'form_comments': CommentForm
                         }
        else:
            context_1 = {'quiz': Quiz.objects.get(id=quiz_id),
                         'comments': Comments.objects.all().filter(
                             quizz_com=Quiz.objects.get(id=quiz_id)),
                         'form_comments': CommentForm,
                         'warning': "Добавлять отзывы могут только зарегистрированные пользователи"}
        return render(self.request, 'details.html', context_1)


class Evaluation(View):
    def get(self, request, quiz_id):
        context = {'quiz': Quiz.objects.get(id=quiz_id),
                   'positions': Positions.objects.all(),
                   'numbers': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
                   }
        return render(self.request, 'criteria.html', context)

    def post(self, request, quiz_id):
        data = request.POST.getlist("mark")
        lst = [item.id for item in Positions.objects.all()]
        users = list(Values.objects.filter(quiz=Quiz.objects.get(id=quiz_id)).all().values("user"))
        users_all = []
        for person in users:
            users_all.append(person["user"])
        if request.user.is_authenticated and request.user.id not in users_all:
            for i in range(0, 5):
                Values.objects.create(position=Positions.objects.get(id=lst[i]),
                                      mark=data[i],
                                      quiz=Quiz.objects.get(id=quiz_id),
                                      user=User.objects.get(id=request.user.id))

            return HttpResponseRedirect("/thanks/")
        elif request.user.is_authenticated and request.user.id in users_all:
            context = {'quiz': Quiz.objects.get(id=quiz_id),
                       'positions': Positions.objects.all(),
                       'numbers': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                       'warning': "Вы уже ранее заполняли анкету"}
            return render(self.request, 'criteria.html', context)
        else:
            context = {'quiz': Quiz.objects.get(id=quiz_id),
                       'positions': Positions.objects.all(),
                       'numbers': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                       'warning': 'Оценить квиз могут только зарегистрированные пользователи'}
            return render(self.request, 'criteria.html', context)


def thanks(request):
    return render(request, 'thanks.html')


def rating(request):
    names = Quiz.objects.all().values("name")
    names_new = []
    for name in names:
        names_new.append(name["name"])
    shares = list(Positions.objects.all().values("share"))
    shares_new = []
    for share in shares:
        shares_new.append(share["share"])

    result_1 = Quiz.objects.filter(quizzes__position__id=1).annotate(
        amount=Avg('quizzes__mark')).order_by('-amount').all()
    result_2 = Quiz.objects.filter(quizzes__position__id=2).annotate(
        amount=Avg('quizzes__mark')).order_by('-amount').all()
    result_3 = Quiz.objects.filter(quizzes__position__id=3).annotate(
        amount=Avg('quizzes__mark')).order_by('-amount').all()
    result_4 = Quiz.objects.filter(quizzes__position__id=4).annotate(
        amount=Avg('quizzes__mark')).order_by('-amount').all()
    result_5 = Quiz.objects.filter(quizzes__position__id=5).annotate(
        amount=Avg('quizzes__mark')).order_by('-amount').all()
    result_new = {}
    for item in names_new:
        result = list(result_1.filter(name=item).all().values("amount"))
        for mark in result:
            a = float(mark["amount"]) * float(shares_new[0] / 100)
            result_new[item] = list()
            result_new[item].append(a)
        result = list(result_2.filter(name=item).all().values("amount"))
        for mark in result:
            result_new[item].append(
                float(mark["amount"]) * float(shares_new[1]) / 100)
        result = list(result_3.filter(name=item).all().values("amount"))
        for mark in result:
            result_new[item].append(
                float(mark["amount"]) * float(shares_new[2]) / 100)
        result = list(result_4.filter(name=item).all().values("amount"))
        for mark in result:
            result_new[item].append(
                float(mark["amount"]) * float(shares_new[3]) / 100)
        result = list(result_5.filter(name=item).all().values("amount"))
        for mark in result:
            result_new[item].append(
                float(mark["amount"]) * float(shares_new[1]) / 100)
    total = {}
    for key, value in result_new.items():
        total[key] = round(sum(result_new[key]), 2)
    total = dict(
        [(k, total[k]) for k in sorted(total, key=total.get, reverse=True)])
    positions = []
    all = list(Positions.objects.all().values("name"))
    for name in all:
        positions.append(name["name"])

    return render(request, 'rating.html',
                  {'result_1': result_1, 'result_2': result_2,
                   'result_3': result_3, 'result_4': result_4,
                   'result_5': result_5, 'total': total,
                   'positions': positions
                   })


class Dates(View):
    def get(self, request):
        context = {'data': DatesPlaces.objects.annotate(
            amount=Count('participation__user')).filter(
            game_date__gte=datetime.now()).select_related('for_quiz').order_by(
            "game_date"),
            'form': FilterForm,
            'text': "Все ближайшие квизы"}
        return render(self.request, 'afisha.html', context)

    def post(self, request):
        if request.POST.get("max_date") >= request.POST.get("min_date"):
            context = {'data': DatesPlaces.objects.annotate(
                amount=Count('participation__user')).filter(
                game_date__gte=request.POST.get("min_date")).filter(
                game_date__lte=request.POST.get("max_date")).select_related(
                'for_quiz').order_by(
                "game_date"),
                'form': FilterForm, 'text': "Результаты поиска"}

        else:
            context = {'data': DatesPlaces.objects.annotate(
                amount=Count('participation__user')).filter(
                game_date__gte=datetime.now()).select_related(
                'for_quiz').order_by(
                'game_date'), 'form': FilterForm,
                'text': "Все ближайшие квизы"}
        return render(self.request, 'afisha.html', context)


class AnketaWrite(View):
    def get(self, request):
        context = {'anketa': Anketa.objects.all()}
        return render(self.request, 'anketa.html', context)

    def post(self, request):
        data = request.POST.getlist("mark")
        users = list(AnketaDone.objects.all().values("user"))
        users_all=[]
        for person in users:
            users_all.append(person["user"])
        if request.user.is_authenticated and request.user.id not in users_all:
            for pk in data:
                AnketaDone.objects.create(
                    user=User.objects.get(id=request.user.id),
                    quest=Point.objects.get(id=int(pk)))
            return HttpResponseRedirect("/anketa_result/")
        elif request.user.is_authenticated and request.user.id in users_all:
            context = {'anketa': Anketa.objects.all(),
                       'warning': "Вы уже ранее заполняли анкету"}
            return render(self.request, 'anketa.html', context)
        else:
            context = {'anketa': Anketa.objects.all(),
                       'warning': "Оставить анкету могут только зарегистрированные пользователи"}
            return render(self.request, 'anketa.html', context)


def anketa_result(request):
    users = list(AnketaDone.objects.all().values("user"))
    users_all = []
    for person in users:
        users_all.append(person["user"])
    number = len(set(users_all))
    note_1 = ""
    note_2 = ""
    if request.user.id in users_all:
        note_1 = "Cпасибо за участие,"
    else:
        note_2 = "Примите участие в анкете,"
    questions = [quest.question for quest in Anketa.objects.all()]
    data_1 = list(Anketa.objects.annotate(
        amount=Count('questions__points__quest')).filter(id=1).all().values(
        'amount', 'questions__option'))
    result_1_option = []
    result_1_amount = []
    for item in data_1:
        result_1_option.append(item['questions__option'])
        result_1_amount.append(item['amount'])
    data_2 = list(Anketa.objects.annotate(
        amount=Count('questions__points__quest')).filter(id=2).all().values(
        'amount', 'questions__option'))
    result_2_option = []
    result_2_amount = []
    for item in data_2:
        result_2_option.append(item['questions__option'])
        result_2_amount.append(item['amount'])
    data_3 = list(Anketa.objects.annotate(
        amount=Count('questions__points__quest')).filter(id=3).all().values(
        'amount', 'questions__option'))
    result_3_option = []
    result_3_amount = []
    for item in data_3:
        result_3_option.append(item['questions__option'])
        result_3_amount.append(item['amount'])
    data_4 = list(Anketa.objects.annotate(
        amount=Count('questions__points__quest')).filter(id=4).all().values(
        'amount', 'questions__option'))
    result_4_option = []
    result_4_amount = []
    for item in data_4:
        result_4_option.append(item['questions__option'])
        result_4_amount.append(item['amount'])
    data_5 = list(Anketa.objects.annotate(
        amount=Count('questions__points__quest')).filter(id=5).all().values(
        'amount', 'questions__option'))
    result_5_option = []
    result_5_amount = []
    for item in data_5:
        result_5_option.append(item['questions__option'])
        result_5_amount.append(item['amount'])
    data_6 = list(Anketa.objects.annotate(
        amount=Count('questions__points__quest')).filter(id=6).all().values(
        'amount', 'questions__option'))
    result_6_option = []
    result_6_amount = []
    for item in data_6:
        result_6_option.append(item['questions__option'])
        result_6_amount.append(item['amount'])
    try:
        os.remove('Quiz/static/data_1.png')
        os.remove('Quiz/static/data_2.png')
        os.remove('Quiz/static/data_3.png')
        os.remove('Quiz/static/data_4.png')
        os.remove('Quiz/static/data_5.png')
        os.remove('Quiz/static/data_6.png')
    except OSError:
        pass
    data_names = result_1_option
    data_values = result_1_amount

    dpi = 80
    fig = plt.figure(dpi=dpi, figsize=(512 / dpi, 384 / dpi))
    mpl.rcParams.update({'font.size': 9})
    plt.title(' (%)')
    xs = range(len(data_names))
    plt.pie(
        data_values, autopct='%.1f', radius=1.1,
        explode=[0.15] + [0 for _ in range(len(data_names) - 1)])
    plt.legend(
        bbox_to_anchor=(-0.16, 0.45, 0.25, 0.25),
        loc='lower left', labels=data_names)
    fig.savefig('Quiz/static/data_1.png')
    plt.close()
    data_names = result_2_option
    data_values = result_2_amount
    dpi = 80
    fig = plt.figure(dpi=dpi, figsize=(512 / dpi, 384 / dpi))
    mpl.rcParams.update({'font.size': 9})
    ax = plt.axes()
    ax.xaxis.grid(True, zorder=1)
    xs = range(len(data_names))
    plt.barh([x + 0.3 for x in xs], [d * 0.9 for d in data_values],
             height=0.2, color='red', alpha=0.7,
             zorder=2)
    plt.yticks(xs, data_names, rotation=10)
    plt.legend(loc='upper right')
    fig.savefig('Quiz/static/data_2.png')
    plt.close()
    data_names = result_3_option
    data_values = result_3_amount
    dpi = 80
    fig = plt.figure(dpi=dpi, figsize=(512 / dpi, 384 / dpi))
    mpl.rcParams.update({'font.size': 9})
    ax = plt.axes()
    ax.xaxis.grid(True, zorder=1)
    xs = range(len(data_names))
    plt.barh([x + 0.3 for x in xs], [d * 0.9 for d in data_values],
             height=0.2, color='red', alpha=0.7,
             zorder=2)
    plt.yticks(xs, data_names, rotation=10)
    plt.legend(loc='upper right')
    fig.savefig('Quiz/static/data_4.png')
    plt.close()
    data_names = result_4_option
    data_values = result_4_amount
    mpl.use('Agg')
    dpi = 80
    fig = plt.figure(dpi=dpi, figsize=(512 / dpi, 384 / dpi))
    mpl.rcParams.update({'font.size': 9})
    plt.title(' (%)')
    xs = range(len(data_names))
    plt.pie(
        data_values, autopct='%.1f', radius=1.1,
        explode=[0.15] + [0 for _ in range(len(data_names) - 1)])
    plt.legend(
        bbox_to_anchor=(-0.16, 0.45, 0.25, 0.25),
        loc='lower left', labels=data_names)
    fig.savefig('Quiz/static/data_4.png')
    plt.close()
    data_names = result_5_option
    data_values = result_5_amount
    dpi = 80
    fig = plt.figure(dpi=dpi, figsize=(512 / dpi, 384 / dpi))
    mpl.rcParams.update({'font.size': 9})
    ax = plt.axes()
    ax.xaxis.grid(True, zorder=1)
    xs = range(len(data_names))
    plt.barh([x + 0.3 for x in xs], [d * 0.9 for d in data_values],
             height=0.2, color='red', alpha=0.7,
             zorder=2)
    plt.yticks(xs, data_names, rotation=10)
    plt.legend(loc='upper right')
    fig.savefig('Quiz/static/data_5.png')
    plt.close()
    data_names = result_6_option
    data_values = result_6_amount
    mpl.use('Agg')
    dpi = 80
    fig = plt.figure(dpi=dpi, figsize=(512 / dpi, 384 / dpi))
    mpl.rcParams.update({'font.size': 9})
    plt.title(' (%)')
    xs = range(len(data_names))
    plt.pie(
        data_values, autopct='%.1f', radius=1.1,
        explode=[0.15] + [0 for _ in range(len(data_names) - 1)])
    plt.legend(
        bbox_to_anchor=(-0.16, 0.45, 0.25, 0.25),
        loc='lower left', labels=data_names)
    fig.savefig('Quiz/static/data_6.png')
    plt.close()
    return render(request, 'anketa_result.html', {'result': number,
                                                  'note_1': note_1,
                                                  'note_2': note_2,
                                                  'data': questions})


class ChangeData(View):
    def get(self, request):
        data = Quiz.objects.filter(quizzes__user=request.user.id).all()
        context = {'anketa': AnketaDone.objects.filter(
            user=User.objects.get(id=request.user.id)).select_related(
            'quest').all(),
                   'value': Values.objects.filter(
                       user=User.objects.get(
                           id=request.user.id)).select_related(
                       'position').select_related('quiz').all(),
                   'comment': Comments.objects.filter(
                       author_com=User.objects.get(
                           id=request.user.id)).select_related(
                       'quizz_com').all(),
                   'names': data.distinct(),
                   'reminder': Participants.objects.select_related(
                       'user').select_related('game').filter(
                       game__game_date__gte=datetime.now()).all()}
        return render(request, 'changes.html', context)

    def post(self, request):
        users = list(User.objects.all().values("username"))
        users_all = []
        for person in users:
            users_all.append(person["username"])
        if ((
                (str(request.POST.get("username")) != str(request.user) and str(
                    request.POST.get("username")) not in users_all)) or (
                str(request.POST.get("username")) == str(request.user))):
            User.objects.filter(username=request.user).update(
                username=request.POST.get("username"),
                email=request.POST.get("email"))
            context = {
                'note': 'Ваши личные данные успешно изменены, будут доступны после обновления страницы',
                'anketa': AnketaDone.objects.filter(
                    user=User.objects.get(id=request.user.id)).select_related(
                    'quest').all(),
                'value': Values.objects.filter(
                    user=User.objects.get(id=request.user.id)).select_related(
                    'quiz').select_related('position').all(),
                'comment': Comments.objects.filter(
                    author_com=User.objects.get(
                        id=request.user.id)).select_related(
                    'quizz_com').all(),
                'names': Quiz.objects.filter(
                    quizzes__user=request.user.id).all().distinct(),
                'reminder': Participants.objects.select_related(
                    'user').select_related('game').filter(
                    game__game_date__gte=datetime.now()).all()}

            return render(request, 'changes.html', context)
        else:
            context = {'note': 'Неверные данные',
                       'anketa': AnketaDone.objects.filter(
                           user=User.objects.get(
                               id=request.user.id)).select_related(
                           'quest').all(),
                       'value': Values.objects.filter(
                           user=User.objects.get(
                               id=request.user.id)).select_related(
                           'quiz').select_related('position').all(),
                       'names': Quiz.objects.filter(
                           quizzes__user=request.user.id).all().distinct(),
                       'comment': Comments.objects.filter(
                           author_com=User.objects.get(
                               id=request.user.id)).select_related(
                           'quizz_com').all(),
                       'reminder': Participants.objects.select_related(
                           'user').select_related('game').filter(
                           game__game_date__gte=datetime.now()).all()}

            return render(request, 'changes.html', context)


class AnketaEdit(View):
    def get(self, request):
        context = {'anketa': Anketa.objects.all()}
        return render(self.request, 'anketa.html', context)

    def post(self, request):
        data = request.POST.getlist("mark")
        AnketaDone.objects.filter(
            user=User.objects.get(id=request.user.id)).delete()
        for pk in data:
            AnketaDone.objects.create(user=User.objects.get(id=request.user.id),
                                      quest=Point.objects.get(id=int(pk)))
        return HttpResponseRedirect("/changes/")


def anketa_delete(request):
    AnketaDone.objects.filter(
        user=User.objects.get(id=request.user.id)).delete()
    return HttpResponseRedirect("/changes/")


def comment_delete(request, com_id):
    Comments.objects.filter(id=com_id).delete()
    return HttpResponseRedirect("/changes/")


class CommentEdit(View):
    def get(self, request, com_id):
        context = {'com': [item.comments_text for item in
                           Comments.objects.filter(id=int(com_id))][0]}
        return render(self.request, 'comments_edit.html', context)

    def post(self, request, com_id):
        Comments.objects.filter(id=com_id).update(
            comments_text=request.POST.get("comments_text"))
        return HttpResponseRedirect("/changes/")


def value_delete(request, name_id):
    Values.objects.filter(quiz=Quiz.objects.get(id=name_id)).delete()
    return HttpResponseRedirect("/changes/")


class ValueEdit(View):
    def get(self, request, name_id):
        context = {'quiz': Quiz.objects.get(id=name_id),
                   'positions': Positions.objects.all(),
                   'numbers': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
                   }
        return render(self.request, 'criteria.html', context)

    def post(self, request, name_id):
        data = request.POST.getlist("mark")
        lst = [item.id for item in Positions.objects.all()]
        for i in range(0, 5):
            Values.objects.filter(quiz=Quiz.objects.get(id=name_id)).update(
                position=Positions.objects.get(id=lst[i]),
                mark=data[i])
        return HttpResponseRedirect("/changes/")


def participant(request, game_id):
    if request.user.is_authenticated and request.user.id not in [person.id for
                                                                 person in
                                                                 Participants.objects.filter(
                                                                     game=DatesPlaces.objects.get(
                                                                         id=game_id)).all()]:
        Participants.objects.create(user=User.objects.get(id=request.user.id),
                                    game=DatesPlaces.objects.get(id=game_id))
        return HttpResponseRedirect("/afisha/")
    else:
        return HttpResponseRedirect("/login/")
