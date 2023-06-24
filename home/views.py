from django.http import request
from django.shortcuts import render
from django.template import context
from django.core.files.storage import FileSystemStorage
from django.core.files import File
from django.conf import settings
import PyPDF2
from .files import *
from .forms import form_view

def index(request):
    form = form_view()
    contents={}
    context={}
    name=''
    contents[name]=''
    if request.method == 'POST':
        if request.POST.get("filter") == "Submit":
            form = form_view(request.POST)
            if form.is_valid():
                x = form.cleaned_data['Skills']
                return result(request,x)

        else:
            uploaded_file = request.FILES['document']
            fs = FileSystemStorage()
            name = fs.save(uploaded_file.name,uploaded_file)
            file_names.append(name)
            temp = settings.MEDIA_ROOT.replace('/media','')
            context['url'] = temp + fs.url(name)
            pd= PyPDF2.PdfReader(context['url'])
            text = pd.pages[0].extract_text()
            temp = text
            str = 'Languages:'
            ind = temp.find(str)
            end = temp.find('CERTIFICATES')
            contents[name] = temp[ind+len(str):end]
            return render(request,'home/index.html',{'form':form})
    return render(request,'home/index.html',{'form':form})

def result(request,x=''):
    contents={'file':''}
    context={}
    for i in file_names:
        contents['file'] += i +":"
        temp = settings.MEDIA_ROOT+'/'
        context['url'] = temp + i
        pd= PyPDF2.PdfReader(context['url'])
        text = pd.pages[0].extract_text()
        temp = text
        str = 'Languages:'
        ind = temp.find(str)
        end = temp.find('CERTIFICATES')
        if x in temp[ind+len(str):end]:
            contents['file'] +=""
        else:
            contents['file'] =""
    return render(request,'home/result.html',{'upload':contents['file']})



