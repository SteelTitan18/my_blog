from django.shortcuts import render
from bloggings.forms import PostForm
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from bloggings.forms import PostForm
from bloggings.models import Post
from bloggings.models import Comment
from bloggings.models import Theme
from django.contrib.auth.decorators import login_required

def home(request):
    postDic = {}
    postList = Post.objects.all()
    themes = Theme.objects.all()
    users = User.objects.all()
    for _post in postList:
        comment = Comment.objects.filter(post = _post).count()
        postDic[_post] = (comment)
    addPost(request)
    return render(request, 'bloggings/index.html', {'postD':postDic, 'themes':themes, 'users': users})

def connexion(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return redirect('connexion')
    return render(request, 'bloggings/login.html')

def sign_up(request):
    if request.method == 'POST':
        username = request.POST['username']
        mail = request.POST['email']
        passw = request.POST['password']
        user = User.objects.create_user(username, mail, passw)
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.save()
        return redirect('home')

    return render(request, 'bloggings/sign_up.html')

# @login_required(login_url='/sign-in/')
def addPost(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            post = Post()
            post.user = request.user
            post.title = request.POST['title']
            post.theme = Theme.objects.get(label=request.POST['theme'])
            post.content = request.POST['content']
            post.save()

            return redirect('home')
    else:
        return redirect('connexion')

    return render(request, 'bloggings/index.html')

def logout_view(request):
    logout(request)
    return redirect('home')
