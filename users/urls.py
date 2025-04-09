from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.register_page, name='signup'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('post-question/', views.post_question, name='post_question'),
    path('like/<int:question_id>/', views.like_question, name='like_question'),
    # path('reply/<int:question_id>/', views.reply_to_question, name='reply_to_question'),
    path('question/<int:question_id>/', views.question_detail, name='question_detail'),
path('reply/<int:reply_id>/', views.reply_to_reply, name='reply_to_reply'),
    path('like-reply/<int:reply_id>/', views.like_reply, name='like_reply'),
    path('r÷eply-to-reply/<int:reply_id>/', views.reply_to_reply, name='reply_to_reply'),
]