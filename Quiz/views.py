from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.db.models import Min, Max, Avg, Count, Sum

from Quiz.forms import UserCreationForm, SearchForm, FilterForm
from django.shortcuts import render, redirect
from django.views.generic import FormView
from django.contrib.auth import login, logout
from django.http import HttpResponseRedirect
from django.views.generic.base import View
from Quiz.models import Quiz, Comments, Positions, Values, DatesPlaces
from django.db.models import Q
from Quiz.forms import CommentForm
from django.contrib.auth.models import User
from datetime import datetime


def main(request):
    return render(request, 'main.html')


class Search(FormView):
    template_name = 'search.html'
    form_class = SearchForm

    def form_valid(self, form):
        data = form.cleaned_data
        result = Quiz.objects.filter((Q(name__contains=data['search']) | (
            Q(category__contains=data['search']))))
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
                quizz_com=new, author_com=request.user
            )
            context_1 = {'quiz': Quiz.objects.get(id=quiz_id),
                         'comments': Comments.objects.all().filter(
                             quizz_com=Quiz.objects.get(id=quiz_id)),
                         'warning': ''
                         }
        else:
            context_1 = {'quiz': Quiz.objects.get(id=quiz_id),
                         'comments': Comments.objects.all().filter(
                             quizz_com=Quiz.objects.get(id=quiz_id)),
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
        positions = list(Positions.objects.all().values("id"))
        lst = []
        for i in positions:
            lst.append(i["id"])
        if request.user.is_authenticated:
            for i in range(0, 5):
                Values.objects.create(position=Positions.objects.get(id=lst[i]),
                                      mark=data[i],
                                      quiz=Quiz.objects.get(id=quiz_id))

            return HttpResponseRedirect("/thanks/")
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
        context = {'data': DatesPlaces.objects.filter(
            game_date__gte=datetime.now()).select_related('for_quiz').order_by(
            "game_date"),
            'form': FilterForm, 'text': "Все ближайшие квизы"}
        return render(self.request, 'afisha.html', context)

    def post(self, request):
        form = FilterForm
        if form.is_valid:
            context = {'data': DatesPlaces.objects.filter(
                game_date__gte=request.POST.get("min_date")).filter(
                game_date__lte=request.POST.get("max_date")).select_related(
                'for_quiz').order_by(
                "game_date"),
                'form': FilterForm, 'text': "Результаты поиска"}

        else:
            context = {'data': DatesPlaces.objects.filter(
                game_date__gte=datetime.now()).select_related(
                'for_quiz').order_by(
                "game_date"),
                'form': FilterForm, 'text': "Все ближайшие квизы"}
        return render(self.request, 'afisha.html', context)
