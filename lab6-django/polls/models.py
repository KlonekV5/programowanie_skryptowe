from django.db import models
import uuid

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

class Token(models.Model):
    value = models.CharField(max_length=200, default=uuid.uuid4, unique=True)
    used = models.BooleanField(default=False)
    relation = models.ManyToManyField(Choice, blank=True)

    def __str__(self):
        return str(self.value) + ';' + str(self.used)

#https://docs.djangoproject.com/en/5.0/ref/models/fields/#django.db.models.ManyToManyField