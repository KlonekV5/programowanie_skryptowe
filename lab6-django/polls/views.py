import uuid
from django.shortcuts import render
from django.http import HttpResponse
from .models import Question, Choice, Token
from django.template import loader


def index(request):
    return HttpResponse('Hello, you are at polls index')


def answers(request):
    latest_question_list = Question.objects.all()
    template = loader.get_template('polls/answers.html')
    context = {
        'latest_question_list': latest_question_list,
    }
    return HttpResponse(template.render(context, request))


def poll(request):
    token = request.GET.get('Token')
    if not token:
        return HttpResponse('Token is missing')

    else:
        try:
            token = Token.objects.get(value=token)
            # token = Token.objects.get_or_create(value=token, used=False)[0] #tokens created 0-99  ?Token=0
        except:
            return HttpResponse('Token is invalid')

        if not token.used:
            latest_question_list = Question.objects.all()
            template = loader.get_template('polls/poll.html')
            context = {
                'latest_question_list': latest_question_list,
                'token': token,
            }
            return HttpResponse(template.render(context, request))

        elif token.used:
            return HttpResponse('Token is already used')


def save(request):
    if request.method == 'GET':
        token = request.GET.get('Token')
        if not token:
            return HttpResponse('Token is missing')

        token = Token.objects.get(value=token)
        if not token.used:
            for item in request.GET:
                if item != 'csrfmiddlewaretoken' and item != 'Token':
                    question = Question.objects.get(question_text=item)
                    selected_choice = Choice.objects.get(choice_text=request.GET[item], question=question.id)
                    selected_choice.votes += 1
                    selected_choice.save()
            token.used = True
            token.save()
            return HttpResponse('Answers saved!')
        else:
            return HttpResponse('Cannot save answer, token is already used')
    else:
        return HttpResponse('Invalid request method')
