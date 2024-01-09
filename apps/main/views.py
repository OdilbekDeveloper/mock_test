from django.shortcuts import render
from .models import *
from django.http import HttpResponse
from django.shortcuts import redirect
# Create your views here.






def Login_Page(request, action_url):
    context = {
        'action_url': action_url,
    }
    return render(request, 'login.html', context=context)



def Get_Listening_Section(request, pk):
    if request.user.is_authenticated:
        listening_section = Listening_section.objects.filter(
            part=pk).order_by('?').first()
        question_number = range(1, listening_section.question_numbers+1)
        context = {
            'listening_section': listening_section,
            'question_number': question_number,
        }
        return render(request, 'listening_section.html', context)
    else:
        return redirect('login')

def add_listening_answers(request):
    if request.method == 'POST':
        section_id = request.POST.get('section_id')
        section = Listening_section.objects.get(id=section_id)
        for i in section.questions.all():
            answer = request.POST.get(str(i.id))
            Listening_answer.objects.create(
                question=i, user_answer=answer, user=request.user)

        return HttpResponse("Answers submitted successfully. You can go back to the telegram bot")


def Get_Reading_Section(request, pk):
    reading_section = Reading_section.objects.filter(
        part=pk).order_by('?').first()
    question_number = range(1, reading_section.question_numbers+1)
    context = {
        'reading_section': reading_section,
        'question_number': question_number,
    }

    return render(request, 'reading_section.html', context)


def add_reading_answers(request):
    if request.method == 'POST':
        section_id = request.POST.get('section_id')
        section = Reading_section.objects.get(id=section_id)
        for i in section.questions.all():
            answer = request.POST.get(str(i.id))
            Reading_answer.objects.create(
                question=i, user_answer=answer, user=request.user)

        return HttpResponse("Answers submitted successfully. You can go back to the telegram bot")


def Get_Writing_Section(request, pk):

    if pk == 1:
        writing_section = Writing_section.objects.filter(
            type=pk).order_by('?').first()
        context = {
            'writing_section': writing_section,
        }

        return render(request, 'writing_section.html', context)

    elif pk == 2:
        writing_section = Writing_section.objects.filter(
            type=pk).order_by('?').first()
        context = {
            'writing_section': writing_section,
        }

        return render(request, 'writing_section2.html', context)


def Add_writing_answers(request):
    if request.method == 'POST':
        answer = request.POST.get('answer')
        section_id = request.POST.get('section_id')
        section = Writing_section.objects.get(id=section_id)
        Writing_answer.objects.create(
            question=section, user_answer=answer, user=request.user)

        return HttpResponse("Answers submitted successfully. You can go back to the telegram bot")


def Finished_Writing_Page(request):
    return render(request, 'finished.html')
