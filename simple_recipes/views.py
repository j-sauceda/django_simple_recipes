# Basic imports
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib import messages  # flash messages
from django.core.paginator import Paginator, EmptyPage  # QuerySet pagination
from django.db.models import Q  # query conditions for QuerySets

# User-related imports
from django.contrib.auth.models import User  # User model
from django.contrib.auth import authenticate, login, logout  # auth functions

# User access decorators
from django.contrib.auth.decorators import login_required
from .decorators import user_is_not_authenticated

# Custom data models
from .models import Article, ArticleComment, ArticlePicture, Category, Profile

# Form classes
from django.contrib.auth.forms import UserCreationForm
from .forms import ArticleForm, ProfileForm


# user register page
@user_is_not_authenticated  # if user already auth, redirect
def registerPage(request):
    # load Form
    form = UserCreationForm()
    # set context
    context = {'form': form}
    # initialize form, clean values, call login and redirect
    if request.method == 'POST':
        # initialize form
        form = UserCreationForm(request.POST)
        if form.is_valid():  # validates form values
            user = form.save(
                commit=False
            )  # does not commit, returns user to be handled manually
            user.username = user.username.lower()  # username to lower case
            user.save()  # now we save the user in the DB
            profile = Profile.objects.create(user=user)
            profile.save()
            login(request, user)  # login the user
            messages.success(
                request,
                'Registration successful. Please, tell us about yourself')
            return redirect('update-profile')
        else:
            for err_msg in form.errors:
                messages.error(request, err_msg)
    # render HTML form
    return render(request, 'simple_recipes/register.html', context)


# login page
@user_is_not_authenticated  # if user already auth, redirect
def loginPage(request):
    # check credentials, call login, redirect
    if request.method == 'POST':
        # read username and pwd from HTML form context
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            # is user in the DB?
            user = User.objects.get(username=username)
        except:
            # if user not in DB, display error
            messages.error(request, 'User does not exist')
        # if user in DB, test username and pwd
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # if username and pwd are correct, login and redirect
            login(request, user)
            return redirect('home')
        else:
            # if username or pwd are wrong, display error
            messages.error(request,
                           'Username or password not found in the database')
    # set context and render HTML form
    context = {}
    return render(request, 'simple_recipes/login.html', context)


# user logout (end session) and redirect
def logoutPage(request):
    logout(request)
    return redirect('login')


# user profile page
def userProfile(request, pk):
    # read user from DB
    user = User.objects.get(id=pk)
    # read profile from DB
    profile = Profile.objects.get(user=user)
    # articles of this author
    articles = Article.objects.filter(author=profile)
    # categories of the author articles
    categories = Category.objects.all()
    # set context
    context = {
        'user': user,
        'profile': profile,
        'articles': articles,
        'categories': categories
    }
    # render profile page
    return render(request, 'simple_recipes/profile.html', context)


# user profile update page
@login_required(login_url='login')  # only logged-in users can access
def updateProfile(request):
    # read User instance from request
    user = User.objects.get(id=request.user.id)
    # read profile from DB
    profile = Profile.objects.get(user=user)
    # initialize Profile form
    form = ProfileForm(instance=profile)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)
        else:
            messages.error(request, 'Invalid form')
            for err in form.errors:
                messages.error(request, form.errors[err][0])
            return redirect('update-profile')
    # set context
    context = {'form': form, 'profile': profile}
    # render update-user HTML form
    return render(request, 'simple_recipes/update_profile.html', context)


# create article page
@login_required(login_url='login')  # only logged-in users can access
def createArticle(request):
    # load Form
    form = ArticleForm()
    # categories available
    categories = Category.objects.all()
    # set context
    context = {
        'categories': categories,
        'form': form,
    }
    # initialize form, clean values, call login and redirect
    if request.method == 'POST':
        # initialize form
        form = ArticleForm(request.POST)
        if form.is_valid():  # validates form values
            article = form.save(
                commit=False
            )  # does not commit, returns user to be handled manually
            user = User.objects.get(id=request.user.id)
            profile = Profile.objects.get(user=user)
            article.author = profile
            article.save()  # now we save the user in the DB
            messages.success(
                request, 'Your new article has been created and published')
            return redirect('read-article', pk=article.id)
        else:
            for err_msg in form.errors:
                messages.error(request, err_msg)
    # render HTML form
    return render(request, 'simple_recipes/article_editor.html', context)


# article page
def readArticle(request, pk):
    # read article from DB
    article = Article.objects.get(id=pk)
    # comments to this article
    comments = ArticleComment.objects.filter(article=article)
    # pictures of this article
    pictures = ArticlePicture.objects.filter(article=article)
    # categories of articles
    categories = Category.objects.all()
    # categories pagination
    cat_paginator = Paginator(categories, 6)
    num_pages = cat_paginator.num_pages
    num_range = range(1, num_pages + 1)
    page_n = 1
    if not request.GET.get('cat_page') in [None, '']:
        page_n = request.GET.get('cat_page')
    try:
        cat_page = cat_paginator.page(page_n)
    except EmptyPage:
        cat_page = cat_paginator.page(1)
        page_n = 1

    # set context
    context = {
        'article': article,
        'comments': comments,
        'categories': cat_page,
        'cat_range': num_range,
        'num_pages': num_pages,
        'page_n': page_n,
        'pictures': pictures,
    }
    # render profile page
    return render(request, 'simple_recipes/article.html', context)


# update article page
@login_required(login_url='login')  # only logged-in users can access
def updateArticle(request, pk):
    # read article from DB
    article = Article.objects.get(id=pk)
    if article.author.user.id != request.user.id:
        messages.error(request, 'You can only edit your own articles')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    # load Form
    form = ArticleForm(instance=article)
    # categories available
    categories = Category.objects.all()
    # set context
    context = {
        'article': article,
        'categories': categories,
        'form': form,
    }
    # initialize form, clean values, call login and redirect
    if request.method == 'POST':
        # initialize form
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():  # validates form values
            article = form.save()
            # article.save()  # now we save the user in the DB
            messages.success(request, 'Your article has been edited')
            return redirect('read-article', pk=article.id)
        else:
            for err_msg in form.errors:
                messages.error(request, err_msg)
    # render HTML form
    return render(request, 'simple_recipes/article_editor.html', context)


# delete article function
@login_required(login_url='login')  # only logged-in users can access
def deleteArticle(request, pk):
    # read article from DB
    article = Article.objects.get(id=pk)
    if article.author.user.id != request.user.id:
        messages.error(request, 'You can only delete your own articles')
        return redirect('home')
    article.delete()
    messages.success(request, 'The article has been deleted')
    return redirect('user-profile', pk=request.user.id)


# create comment function
@login_required(login_url='login')  # only logged-in users can access
def createComment(request, pk):
    # read user from DB
    user = User.objects.get(id=request.user.id)
    # read profile from DB
    profile = Profile.objects.get(user=user)
    # read article from DB
    article = Article.objects.get(id=pk)
    # create comment
    text_input = ''
    if request.method == 'POST':
        text_input = request.POST.get('new_comment')
    if text_input == '':
        messages.warning(request, 'Empty comment')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    new_comment = ArticleComment.objects.create(article=article,
                                                commentor=profile,
                                                text=text_input)
    new_comment.save()
    messages.success(request, 'Your comment has been posted')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# delete comment function
@login_required(login_url='login')  # only logged-in users can access
def deleteComment(request, art_pk, comm_pk):
    # read user from DB
    user = User.objects.get(id=request.user.id)
    # read profile from DB
    profile = Profile.objects.get(user=user)
    # read article from DB
    article = Article.objects.get(id=art_pk)
    # fetch comment
    comment = ArticleComment.objects.get(id=comm_pk, article=article)
    if comment.commentor != profile:
        messages.error(request, 'You can only delete the comments you wrote')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    comment.delete()
    messages.success(request, 'Your comment has been deleted')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# request user contact link
@login_required(login_url='login')  # only logged-in users can access
def uploadPictures(request, pk):
    # read user from DB
    user = User.objects.get(id=request.user.id)
    # read article from DB
    article = Article.objects.get(id=pk)
    if article.author.user != user:
        messages.error(request,
                       'You can only upload pictures to your own articles')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    # handle POST request
    if request.method == 'POST':
        # loop through multiple image uploads
        for file in request.FILES.getlist('image'):
            # create ArticlePicture object and save
            photo = ArticlePicture.objects.create(article=article, image=file)
            photo.save()
    messages.success(request, 'Your picture(s) have been uploaded')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# cancel contact request link
@login_required(login_url='login')  # only logged-in users can access
def deletePicture(request, pk):
    # read photo from DB
    photo = ArticlePicture.objects.get(image=pk)
    # read user from DB
    user = User.objects.get(id=request.user.id)
    # read article from DB
    if photo.article.author.user != user:
        messages.error(request,
                       'You can only delete pictures of your own articles')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    # delete photo
    photo.delete()
    messages.success(request, 'The picture has been deleted')
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# Home Page
def home(request):
    # import pdb;pdb.set_trace()
    # q: query variable
    q = ''
    if request.GET.get('q') != None:
        q = request.GET.get('q')
    # cat: query variable
    cat = ''
    if request.GET.get('cat') != None:
        cat = request.GET.get('cat')
    # articles
    if not cat in [None, '']:
        articles = Article.objects.filter(Q(categories__name=cat))
    else:
        articles = Article.objects.filter(
            Q(title__icontains=q) | Q(body__icontains=q))  #.distinct()
    # articles pagination
    art_paginator = Paginator(articles, 3)
    art_pages = art_paginator.num_pages
    art_range = range(1, art_pages + 1)
    art_page_n = 1
    if not request.GET.get('art_page') in [None, '']:
        art_page_n = request.GET.get('art_page')
    try:
        art_page = art_paginator.page(art_page_n)
    except EmptyPage:
        art_page = art_paginator.page(1)
        art_page_n = 1

    # article pictures
    article_pictures = ArticlePicture.objects.filter(article__in=art_page)

    # categories of articles
    categories = Category.objects.all()
    # categories pagination
    cat_paginator = Paginator(categories, 6)
    num_pages = cat_paginator.num_pages
    num_range = range(1, num_pages + 1)
    page_n = 1
    if not request.GET.get('cat_page') in [None, '']:
        page_n = request.GET.get('cat_page')
    try:
        cat_page = cat_paginator.page(page_n)
    except EmptyPage:
        cat_page = cat_paginator.page(1)
        page_n = 1

    # set context
    context = {
        'articles': art_page,
        'art_range': art_range,
        'art_pages': art_pages,
        'art_page_n': art_page_n,
        'article_pictures': article_pictures,
        'categories': cat_page,
        'cat_range': num_range,
        'num_pages': num_pages,
        'page_n': page_n,
    }
    return render(request, 'simple_recipes/index.html', context)
