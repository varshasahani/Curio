from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth import get_user_model

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=True)
    admin = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

User = get_user_model()

class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="questions")
    title = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Reply(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="replies")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="replies")
    parent_reply = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name="child_replies")
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.parent_reply:
            return f"Reply by {self.user.username} to Reply: {self.parent_reply.body[:30]}..."
        return f"Reply by {self.user.username} on {self.question.title}"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="likes")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, null=True, blank=True, related_name="likes")
    reply = models.ForeignKey(Reply, on_delete=models.CASCADE, null=True, blank=True, related_name="likes")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'question')  # Ensure a user can like a question only once

    def __str__(self):
        if self.question:
            return f"Like by {self.user.email} on Question: {self.question.title}"
        elif self.answer:
            return f"Like by {self.user.email} on Answer: {self.answer.body[:30]}..."
        return f"Like by {self.user.email}"