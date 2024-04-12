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
        token = Token.objects.create(value=str(uuid.uuid4()), used=False)
        request.session['Token'] = token.value


    session_token = request.session.get('Token')
    if not session_token:
        return HttpResponse('Error: no token')
    token = Token.objects.get(value=session_token)
    if not token.used:
        latest_question_list = Question.objects.all()
        template = loader.get_template('polls/poll.html')
        context = {
            'latest_question_list': latest_question_list,
            'token' : token
        }
        return HttpResponse(template.render(context, request))
    elif token.used:
        return HttpResponse('Error: Token already used')
    else:
        return HttpResponse('Unknown Error!')


def save(request):
    if request.method == 'GET':
        token = request.GET.get('Token')
        if token:
            token = Token.objects.get(value=token)
            if not token.used:
                for item in request.GET:
                    if item != 'csrfmiddlewaretoken':
                        question = Question.objects.get(question_text=item)
                        selected_choice = Choice.objects.get(choice_text=request.GET[item], question=question.id)
                        selected_choice.votes += 1
                        selected_choice.save()
                        token.used = True
                        token.save()
                return HttpResponse('Answers saved!')
            elif token.used:
                return HttpResponse('Error: Token already used')
            else:
                return HttpResponse('Unknown Error!')
        else:
            return HttpResponse('Error: No Token')
