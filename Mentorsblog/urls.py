"""Mentorsblog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include
from django.conf.urls import url
from myapp import views


from django.contrib.auth import views as auth_views
from django.contrib.auth import login as auth_login
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [



    path('admin/', admin.site.urls),
    url('index/',views.index,name='index'),

    url('login/',views.login,name='login'),
    url('logout/',views.logout,name='logout'),
    url('register/',views.Register,name='register'),



#forgot password
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='password_reset_form.html'),name='password_reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'),name='password_reset_complete'),
#cnagge password
     url('changepass/',views.change_password,name='changepass'),





#user profile

    url('editprofile/',views.edit_profile,name='editprofile'),
    url('viewprofile/',views.view_profile,name='viewprofile'),
    url('team/',views.team,name='team'),
    url('aboutus/',views.aboutus,name='aboutus'),
    url('feedback/',views.feedback,name='feedback'),


  #comment on post
     url('postcomment', views.postcomment, name='postcomment'),
      # blog images
     url('photos/', views.photo, name='photos'),
      url('imagesearch/', views.search_photos, name='imagesearch'),

    #Detailv of post
     url('(?P<id>[0-9]+)/$', views.d, name='d'),

    #allblogs
     url('allblogs/', views.allblogs, name='allblogs'),
    url('alsearch/', views.search_allblogs, name='alsearch'),

#like on post
     url('like/', views.like_post, name='like-post'),



#vedio
     url('video/', views.video, name='video'),
     url('videoosearch/', views.search_video, name='videsoosearch'),


    # blog vedios


   #blog pdf
    url('postpdf/', views.pdf, name='pdf'),
     url('pdfsearch/', views.search_pdf, name='pdfsearch'),




    #path('like/<int:pk>',LikeView, name='like_post'),

#assignments
    url('assignments/', views.assignment, name='assignments'),

    url('assignmentsearch/', views.search_assignment, name='assignmentsearch'),


#upload assignment
      url('viewassignment/', views.view_assignment, name='viewassignment'),
      url('uploadassignment/', views.upload_assignment, name='uploadassignment'),




]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
