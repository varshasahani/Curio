from django.contrib import admin
from .models import User, Question, Reply, Like

# Register your models here.
# Register your models here
admin.site.register(Question)
admin.site.register(Reply)
admin.site.register(Like)