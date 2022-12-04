from django.conf import settings
from django.core.checks import messages
from django.db.models.fields import CharField
from django.forms.widgets import Input
from django.http import HttpResponse
from django.shortcuts import render,redirect
from . forms import *
from django.contrib import messages
from django.views import generic
from youtubesearchpython import VideosSearch
import requests
import wikipedia
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.template import loader

# Create your views here.

def home(request):
    return render(request,'dashboard/home.html')

@login_required
def notes(request):
    if request.method=="POST":
        form=NotesForm(request.POST)
        if form.is_valid():
            notes=Notes(user=request.user,title=request.POST['title'],description=request.POST['description'])
            notes.save()
        messages.success(request,f"Notes Added from {request.user.username} Successfully")
        return redirect('notes')
    else:
            
        form=NotesForm()
    notes=Notes.objects.filter(user=request.user)
    context={'notes':notes,'form':form}
    return render(request,'dashboard/notes.html',context)



class NotesDetailView(generic.DetailView):
    model=Notes

@login_required
def delete_note(request,pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect("notes")


@login_required
def homework(request):

    if request.method=="POST":
        form = HomeworkForm(request.POST)
        if form.is_valid():
            try:
                finished=request.POST['is_finished']
                if finished=="on":
                    finished=True
                else:
                    finished=False
            except:
                finished=False
            homeworks=Homework(
                user=request.user,
                subject=request.POST['subject'],
                title=request.POST['title'],
                description=request.POST['description'],
                due=request.POST['due'],
                is_finished=finished
            )
            homeworks.save()
            messages.success(request,f'Homework Added from {request.user.username}!!')
            return redirect('homework')
    else:
          form=HomeworkForm()
              
    homework=Homework.objects.filter(user=request.user)

    if len(homework)==0:
        homework_done= True
    else:
        homework_done=False
    context={'homeworks':homework,
        'homeworks_done':homework_done,
        'form':form,
    }
    return render(request,'dashboard/homework.html',context)
    
    
@login_required
def update_homework(request, pk=None):
    homework=Homework.objects.get(id=pk)
    if homework.is_finished== True:
        homework.is_finished=False
    else:
        homework.is_finished=True
    homework.save()
    return redirect('homework')


@login_required
def delete_homework(request,pk=None):
    Homework.objects.get(id=pk).delete()
    return redirect("homework")


def youtube(request):
    if request.method=="POST":
        form=DashboardForm(request.POST)
        text=request.POST['text']
        video=VideosSearch(text,limit=10)
        result_list=[]
        for i in video.result()['result']:
            result_dict={
                'input':text,
                'title':i['title'],
                'duration':i['duration'],
                'thumbnail':i['thumbnails'][0]['url'],
                'channel':i['channel']['name'],
                'link':i['link'],
                'views':i['viewCount']['short'],
                'published':i['publishedTime']

            }
            desc=''
            if i['descriptionSnippet']:
                for j in i['descriptionSnippet']:
                    desc+=j['text']
            result_dict['description']=desc
            result_list.append(result_dict)
            context={
                'form':form,
                'results':result_list
            }
        return render(request,'dashboard/youtube.html',context)
    else:
        form=DashboardForm()
        form=DashboardForm()
        context={'form':form}
    return render(request,'dashboard/youtube.html',context)    


@login_required
def todo(request):
    return render(request,'dashboard/todo.html')



def books(request):
    if request.method=="POST":
        form=DashboardForm(request.POST)
        text=request.POST['text']
        url="https://www.googleapis.com/books/v1/volumes?q="+text
        r=requests.get(url)
        answer=r.json()
        result_list=[]
        for i in range(10):
            result_dict={
                'title':answer['items'][i]['volumeInfo']['title'],
                 'subtitle':answer['items'][i]['volumeInfo'].get('subtitle'),
                 'description':answer['items'][i]['volumeInfo'].get('description'),
                 'count':answer['items'][i]['volumeInfo'].get('pageCount'),
                 'categories':answer['items'][i]['volumeInfo'].get('categories'),
                 'rating':answer['items'][i]['volumeInfo'].get('pageRating'),
                 'thumbnail':answer['items'][i]['volumeInfo'].get('imageLinks').get('thumbnail'),
                 'preview':answer['items'][i]['volumeInfo'].get('previewLink')
            }
            result_list.append(result_dict)
            context={
                'form':form,
                'results':result_list
            }
        return render(request,'dashboard/books.html',context)
    else:
        form=DashboardForm()
    form=DashboardForm()
    context={'form':form}
    return render(request,'dashboard/books.html',context)
   
    
@login_required
def dictionary(request):
    
    return render(request,'dashboard/home.html')
          

@login_required
def wiki(request):
    if request.method=='POST':
        text=request.POST['text']
        form=DashboardForm(request.POST)
        search=wikipedia.page(text)
        context={
            'form':form,
            'title':search.title,
            'link':search.url,
            'details':search.summary
        }
        return render(request,'dashboard/wiki.html',context)
    else:

        form=DashboardForm()
        context={
            'form':form
        }
    return render(request,'dashboard/wiki.html',context)




def register(request):
    if request.method=='POST':
        form=UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            
            reg = request.POST.get('username')
            messages.success(request,'Account created for - ' + reg)
            return redirect("register")
    else:
        form=UserRegistrationForm()
    context={
            'form':form
        }
           
    return render(request,'dashboard/register.html',context)


@login_required
def profile(request):
    homeworks=Homework.objects.filter(is_finished=False,user=request.user)
    
    if len(homeworks)==0:
        homework_done=True
    else:
        homework_done=False
    
    context={
        'homeworks':homeworks,
        'homework_done':homework_done,
        
    }
    return render(request,"dashboard/profile.html",context)


@login_required
def complain(request):
	
	return render(request,"dashboard/home.html")


@login_required
def contact(request):

	return render (request, 'dashboard/home.html')			
 
def error_404(request, exception):
    return render(request,"dashboard/404.html") 

def error_500(request):
    return render(request,"dashboard/500.html") 


