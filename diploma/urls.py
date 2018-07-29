"""diploma URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls import include, url
from Quiz import views
from django.conf.urls.static import static
from diploma import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', views.main, name='main'),
    url(r'^search/$', views.Search.as_view(), name='search'),
    url(r'^result/$', views.Search.as_view()),
    url(r'^catalog/', include(
        [url('^$', views.about_quiz, name='quiz_all'),
         url(r'^(\d+)/',
             include([url('^$', views.Details.as_view(), name='quiz'),
                      url(r'^criteria/$', views.Evaluation.as_view(),
                          name='criteria')]))])),
    url(r'^register/$', views.RegisterFormView.as_view(), name='register'),
    url(r'^login/$', views.LoginFormView.as_view(), name='login'),
    url(r'^logout/$', views.LogoutView.as_view(), name='logout'),
    url(r'^rating/$', views.rating, name='rating'),
    url(r'^afisha/$', views.Dates.as_view(), name='afisha'),
    url(r'^thanks/$', views.thanks, name='thanks'),
]
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
