from django.shortcuts import render
from bloggings.forms import PostForm
from bloggings.forms import CommentForm
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from bloggings.models import Post
from bloggings.models import Comment
from bloggings.models import Theme
from django.contrib.auth.decorators import login_required
import django.views.generic as gnr
from django.views.generic.edit import CreateView
from django.contrib import messages
# import operator
# from functools import reduce
# from django.views.generic.list import ListView
# from django.db.models import Q

def home(request):
    postDic = {}
    postList = Post.objects.all()
    themes = Theme.objects.all()

    for _post in postList:
        comment = Comment.objects.filter(post = _post).count()
        postDic[_post] = (comment)
    addPost(request)
    return render(request, 'bloggings/index.html', {'postD':postDic, 'themes':themes})

# class PostListView(gnr.ListView):
#     template_name = 'bloggings/index.html'
#
#     def get(self, request):
#         postDic = {}
#         queryset = Post.objects.all()
#         for _post in queryset:
#             comment = Comment.objects.filter(post = _post).count()
#             postDic[_post] = (comment)
#         return render(request, self.template_name, {'postDic':postDic})

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

@login_required(login_url='/sign-in/')
def addPost(request):
    request.POST._mutable = True
    # messages.add_message(request, messages.INFO,"Vous devez être connecté !")
    if request.method == 'POST':
        post = Post()
        post.user = request.user
        # post.title = request.POST['title']
        # post.theme = Theme.objects.get(label=request.POST['theme'])
        # post.content = request.POST['content']
        # post.save()
        form = PostForm(request.POST, instance=post)
        if request.POST["theme"] == "" and request.POST["new_theme"] != "":
            theme = Theme()
            theme.label = request.POST["new_theme"]
            theme.save()
            request.POST["theme"] = theme
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PostForm()

    return render(request, 'bloggings/addPost.html', {'form':form})

def logout_view(request):
    logout(request)
    return redirect('home')

def DetailPost(request, post_id):
    _post = Post.objects.get(id = post_id)
    comments = Comment.objects.filter(post = _post)
    my_post = []
    if request.user.is_authenticated:
        my_post = Post.objects.filter(user = request.user)

    if request.method == 'POST':
        comment = Comment()
        if request.user.is_authenticated:
            comment.user = request.user
            comment.post = Post.objects.get(id = post_id)
            form = CommentForm(request.POST, instance=comment)
            if form.is_valid():
                comment = form.save()
                return redirect("details", post_id)
        else:
            messages.add_message(request, messages.INFO,"Vous devez être connecté !")
            return redirect("connexion")
    else:
        form = CommentForm()

    return render(request, 'bloggings/post_detail.html', {'post': _post, 'comments':comments, 'my_post':my_post, 'form':form})

def my_posts(request):
    postDic = {}
    postList = Post.objects.filter(user = request.user)
    themes = Theme.objects.all()

    for _post in postList:
        comment = Comment.objects.filter(post = _post).count()
        postDic[_post] = (comment)
    addPost(request)
    return render(request, 'bloggings/my_posts.html', {'postD':postDic, 'themes':themes})

def profile(request):
    return render(request, 'bloggings/user_profile.html')

def modif_profile(request):
    redirection = 'profile'
    if request.method == 'POST':
        user = request.user
        pseudo = user.username
        user.username = request.POST['username']
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        if user == authenticate(username = pseudo, password = request.POST['old_password']):
            user.set_password(request.POST['new_password'])
            redirection = 'connexion'
        user.save()

        return redirect('connexion')

    return render(request, 'bloggings/modif_profile.html')

def post_delete(request, post_id):
    post = Post.objects.get(id = post_id)
    post.delete()
    return redirect('my-posts')

    return render(request, 'listings/my_posts.html', {'post':post})

def post_update(request, post_id):
    post = Post.objects.get(id = post_id)

    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('details', post.id)
    else:
        form = PostForm(instance=post)

    return render(request, 'bloggings/post_update.html', {'form':form})

@login_required(login_url='/sign-in/')
def index_like(request, post_id):
    post = Post.objects.get(id = post_id)
    post.like = post.like + 1
    post.save()

    return redirect('home')

@login_required(login_url='/sign-in/')
def index_dislike(request, post_id):
    post = Post.objects.get(id = post_id)
    post.dislike = post.dislike + 1
    post.save()

    return redirect('home')

@login_required(login_url='/sign-in/')
def detail_like(request, post_id):
    post = Post.objects.get(id = post_id)
    post.like = post.like + 1
    post.save()

    return redirect('details', post.id)

@login_required(login_url='/sign-in/')
def detail_dislike(request, post_id):
    post = Post.objects.get(id = post_id)
    post.dislike = post.dislike + 1
    post.save()

    return redirect('details', post.id)

@login_required(login_url='/sign-in/')
def my_post_like(request, post_id):
    post = Post.objects.get(id = post_id)
    post.like = post.like + 1
    post.save()

    return redirect('my-posts')

@login_required(login_url='/sign-in/')
def my_post_dislike(request, post_id):
    post = Post.objects.get(id = post_id)
    post.dislike = post.dislike + 1
    post.save()

    return redirect('my-posts')

@login_required(login_url='/sign-in/')
def comment_like(request, post_id, comment_id):
    post = Post.objects.get(id = post_id)
    comment = Comment.objects.get(id = comment_id)
    comment.like = comment.like + 1
    comment.save()

    return redirect('details', post.id)

@login_required(login_url='/sign-in/')
def comment_dislike(request, post_id, comment_id):
    post = Post.objects.get(id = post_id)
    comment = Comment.objects.get(id = comment_id)
    comment.dislike = comment.dislike + 1
    comment.save()

    return redirect('details', post.id)

# class PostSearchListView(ListView):
#     model = Post
#     context_object_name = "post_lst"
#     template_name = "bloggings/index.html"
#     paginate_by = 10
#
#     def get_queryset(self):
#         result = super(PostSearchListView, self).get_queryset()
#
#         query = self.request.GET.get('q')
#         if query:
#             query_list = query.split()
#             result = result.filter(
#                 reduce(operator.and_,
#                        (Q(title__icontains=q) for q in query_list)) |
#                 reduce(operator.and_,
#                        (Q(content__icontains=q) for q in query_list))
#             )
#
#         return result

# class DetailPost(gnr.DetailView):
#     template_name = 'bloggings/post_detail.html'
#     model = Post

# @login_required(login_url='/sign-in/')
# def Commenting(request, post_id):
#
#     # comment = Comment()
#     # comment.user = request.user
#     # comment.post = Post.objects.get(id = post_id)
#     if request.method == 'POST':
#         print("okk")
#
#         comment = Comment()
#         comment.user = request.user
#         comment.post = Post.objects.get(id = post_id)
#         form = CommentForm(request.POST, instance=comment)
#         if form.is_valid():
#             comment = form.save()
#             return redirect("details", post_id)
#     else:
#         form = CommentForm()
#     return render(request, 'bloggings/comment.html', {'form':form})

# class Commenting(CreateView):
#     template_name = 'bloggings/comment.html'
#     model = Comment
#     fields = ['content']
#     success_url = 'details'
#
#     # @login_required(login_url='/sign-in/')
#     def post(self, request, pk):
#         comment = Comment()
#         comment.user = self.request.user
#         comment.post = Post.objects.get(id = pk)
#         form = CommentForm(instance=comment)
#         if form.is_valid():
#             comment = form.save()
#             return redirect('details')
#         else:
#             form = CommentForm(instance=comment)
#         return render(request, self.template_name, {'form':form})
