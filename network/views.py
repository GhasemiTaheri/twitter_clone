import json
from django.contrib.auth import authenticate, login, logout
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


def load_post(request, type):
    if type == "all":
        posts = Post.objects.all().order_by("-create_date")
    elif type == "following":
        posts = Post.objects.filter(owner__in=request.user.followers.all()).order_by("-create_date")

    return JsonResponse([post.serialize(request.user) for post in posts], safe=False)


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
