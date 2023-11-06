from django.shortcuts import render,redirect
from django.contrib import messages
from .form import CustomUserForm
from .models import News,Category,Comment
from django.contrib.auth import authenticate, login

#  Home Page
def home(request):
    first_news=News.objects.first()
    three_news=News.objects.all()[1:4]
    three_categories=Category.objects.all()[0:3]

    return render(request, 'home.html',{
        'first_news':first_news,
        'three_news':three_news,
        'three_categories':three_categories

    })

# All News Page
def all_news(request):
    all_news=News.objects.all()
    return render(request, 'all-news.html',{
        'all_news':all_news
    })

# Deatil Page
def detail(request,id):
    news=News.objects.get(pk=id)
    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        comment=request.POST['message'] 
        Comment.objects.create(
            news=news,
            name=name,
            email=email,
            comment=comment
        )
        messages.success(request,'comment submitted but in moderation mode.')
    category=Category.objects.get(id=news.category.id)
    rel_news=News.objects.filter(category=category).exclude(id=id)
    comments=Comment.objects.filter(news=news,status=True).order_by('-id')
    return render(request, 'detail.html',{
        'news':news,
        'related_news':rel_news,
        'comments':comments
    })

#fetch all category
def all_category(request):
    cats=Category.objects.all()
    return render(request,'category.html',{
        'cats':cats
    })

#fetch news in category
def category(request,id):
    category=Category.objects.get(id=id)
    news=News.objects.filter(category=category)
    return render(request,'category-news.html',{
        'all_news':news,
        'category':category
    })

def registro(request):
    if request.method == 'POST':
        formulario = CustomUserForm(request.POST)  # Crea una instancia del formulario
        if formulario.is_valid():
            user = formulario.save()  # Guarda el usuario
            user = authenticate(username=formulario.cleaned_data["username"], password=formulario.cleaned_data["password1"])
            login(request, user)
            return redirect('home')
    else:
        formulario = CustomUserForm()  # Instancia un formulario en blanco si es un GET request

    data = {'form': formulario}  # Pasar la instancia del formulario en el diccionario

    return render(request, '/registro.html', data)
