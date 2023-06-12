from django.shortcuts import render, redirect, get_object_or_404
from .forms import Profile_form, Post_form, Photo_form, Comment_post_form, Comment_photo_form, MessageForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from .models import Profile, Post, Comment_post, Photo, Comment_photo, Message
from django.urls import reverse
from django.http import HttpResponse

def register(request):
	if request.method == "POST":
		register_form = UserCreationForm(request.POST)
		if register_form.is_valid():
			user = register_form.save()
			user_name = user.username
			profile = Profile.objects.create(user=user, nickname=user_name)
			login(request, user)
			return redirect("/my_profile/")

	else:
		register_form = UserCreationForm()
		return render (request, "social_network/register.html", {"register_form":register_form})

def login_view(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data["username"]
			password = form.cleaned_data["password"]
			user = authenticate(request, username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("home")
			else:
				messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request, "social_network/login.html", {"login_form":form})

def logout_view(request):
	logout(request) 
	return redirect("register")

def my_profile(request):
	profile = request.user.profile
	user_posts = Post.objects.filter(user=profile)
	user_photos = Photo.objects.filter(user=profile)
	all_items = list(user_posts) + list(user_photos)
	all_items = sorted(all_items, key=lambda item: item.pub_date, reverse=True)
    
	return render(request, 'social_network/my_profile.html', {'profile': profile, 'items': all_items})

def profile(request, nickname):
    other_profile = get_object_or_404(Profile, nickname=nickname)
    user = request.user
    is_following = user.profile.follow.filter(id=other_profile.id).exists()

    if request.method == 'POST':
        if is_following:
            user.profile.follow.remove(other_profile)
        else:
            user.profile.follow.add(other_profile)
        return redirect('profile', nickname=nickname)

    return render(request, 'social_network/profile.html', {'profile': other_profile, "is_following": is_following})

def setting(request):
	if request.method == 'POST':
		form = PasswordChangeForm(request.user, request.POST)
		if form.is_valid():
			user = form.save()
			update_session_auth_hash(request, user)
			messages.success(request, 'Password changed successful')
			return redirect("/my_profile/")
	form = PasswordChangeForm(request.user)
	return render(request, "social_network/set_password.html",{"form":form})

def set_profile(request):
	profile = Profile.objects.get(user=request.user)
	if request.method == 'POST':
		form = Profile_form(request.POST, instance=profile)
		if form.is_valid():
			form.save()
			return redirect('/my_profile/')
	else:
		form = Profile_form(instance=profile)

	return render(request, 'social_network/set_profile.html', {'form':form})

def search(request):
	return render(request, 'social_network/search.html')

def livesearch(request, word, sid1, sid2):
	profiles = Profile.objects.filter(nickname__icontains=word)

	if len(profiles) > 0:
		response = ''
		for profile in profiles:
			response += '<a href="' + reverse('profile', args=(profile.nickname,)) + f'">{profile.nickname}</a><br/>'

	else:
		response = 'User does not exist.'

	return HttpResponse(response)
def add_post(request):
	if request.method == 'POST':
		form = Post_form(request.POST)
		if form.is_valid():
			post = form.save(commit=False)
			post.user = request.user.profile
			post.save()
			return redirect('home')
	else:
		form = Post_form()
	return render(request, 'social_network/add_post.html', {'form': form})

def add_photo(request):
	if request.method == 'POST':
		form = Photo_form(request.POST)
		if form.is_valid():
			title = form.cleaned_data['title']
			picture = request.FILES['picture']
			photo = Photo(user=request.user.profile, title=title, picture=picture)
			photo.save()
			return redirect('home')
	else:
		form = Photo_form()
	return render(request, 'social_network/add_photo.html', {'form': form})

def home(request):
	user = request.user.profile
	user_posts = Post.objects.filter(user=user)
	user_photos = Photo.objects.filter(user=user)
	followed_profiles = user.follow.all()
	followed_posts = Post.objects.filter(user__in=followed_profiles)
	followed_photos = Photo.objects.filter(user__in=followed_profiles)
	all_items = list(user_posts) + list(user_photos) + list(followed_posts) + list(followed_photos)
	all_items = sorted(all_items, key=lambda item: item.pub_date, reverse=True)
    
	return render(request, 'social_network/home.html', {'items': all_items})

def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    comments = Comment_post.objects.filter(post=post)
    
    if request.method == 'POST':
        form = Comment_post_form(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', post_id=post_id)
    else:
        form = Comment_post_form()
    
    return render(request, 'social_network/post_detail.html', {'post': post, 'comments': comments, 'form': form})

def photo_detail(request, post_id):
    post = get_object_or_404(Photo, pk=post_id)
    comments = Comment_photo.objects.filter(post=post)
    
    if request.method == 'POST':
        form = Comment_photo_form(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('photo_detail', post_id=post_id)
    else:
        form = Comment_post_form()
    
    return render(request, 'social_network/photo_detail.html', {'post': post, 'comments': comments, 'form': form})

def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.user, request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            return redirect('inbox') 
    else:
        form = MessageForm(request.user)
    return render(request, 'social_network/message_form.html', {'form': form})

def inbox(request):
    user = request.user
    messages = Message.objects.filter(recipient=user, is_read=False)
    return render(request, 'social_network/inbox.html', {'messages': messages})

def read_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    message.is_read = True
    message.save()
    return render(request, 'social_network/read_message.html', {'message': message})