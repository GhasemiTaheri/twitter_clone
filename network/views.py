import json
from django.contrib.auth import authenticate, login, logout
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post


def index(request):
    return render(request, "network/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")


@csrf_exempt
def new_post(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    post = Post.objects.create(text=data['post_content'], owner_id=request.user.id)
    post.save()
    return JsonResponse({"success": "post add successfully"}, status=201)


def load_post(request):
    if request.path == "/":
        posts = Post.objects.all().order_by("-create_date")
    elif request.path == "/following-post":
        posts = Post.objects.filter(owner__in=request.user.followers.all()).order_by("-create_date")

    paginator = Paginator(posts, 10)
    page_num = request.GET.get('page_num')
    try:
        posts = paginator.page(page_num)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, "network/index.html", {'posts': posts, 'page': page_num})


def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    if request.method == "POST":
        if user in request.user.followers.all():
            request.user.followers.remove(user)
        else:
            request.user.followers.add(user)

        return HttpResponseRedirect(reverse('profile_view', kwargs={'username': username}))

    it_self = False
    follow = False
    if user == request.user:
        it_self = True
    else:
        if user in request.user.followers.all():
            follow = True

    return render(request, 'network/profile.html', {
        'profile': user,
        'it_self': it_self,
        'follow': follow
    })


@csrf_exempt
def update_post(request):
    if request.method != "PUT":
        return JsonResponse({"error": "PUT request required."}, status=400)

    data = json.loads(request.body)
    post = Post.objects.get(id=data['post_id'])
    if post.owner == request.user:
        post.text = data['content']
        post.save()
    else:
        return JsonResponse({"error": "post updated faild"}, status=400)
    return JsonResponse({"success": "post updated successfully"}, status=201)


@csrf_exempt
def like_post(request):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)

    data = json.loads(request.body)
    post = Post.objects.get(id=data['post_id'])
    if post.likes.filter(id=request.user.id):
        post.likes.remove(request.user.id)
        return JsonResponse({"status": "remove like"}, status=201)
    else:
        post.likes.add(request.user.id)
        return JsonResponse({"status": "add like"}, status=201)
