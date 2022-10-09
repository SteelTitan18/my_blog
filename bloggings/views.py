from django.shortcuts import render
from bloggings.forms import PostForm
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from bloggings.forms import PostForm
from bloggings.models import Post
from bloggings.models import Comment

def home(request):
    postDic = {}
    postList = Post.objects.all()
    themes = Theme.objects.all()
    for _post in postList:
        comment = Comment.objects.filter(post = _post).count()
        # commentNb.append(Post.objects.raw('SELECT COUNT(*) FROM blogging_comment WHERE post = post'))
        postDic[_post] = (comment)
        # print(postDic)
        # print(type(_post))

    return render(request, 'bloggings/index.html', {'postD':postDic, 'themes':themes})

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
