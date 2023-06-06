from django.forms import ModelForm, Form, BooleanField
from .models import Profile, Post, Photo, Comment_post, Comment_photo, Message
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User


class Profile_form(ModelForm):
	class Meta:
		model = Profile
		fields = ['bio', 'profile_picture']

class Post_form(ModelForm):
	class Meta:
		model = Post
		fields = ['title', 'text']

class Comment_post_form(ModelForm):
	class Meta:
		model = Comment_post
		fields = ['text']

class Photo_form(ModelForm):
	class Meta:
		model = Photo
		fields = ['title', 'picture']

class Comment_photo_form(ModelForm):
	class Meta:
		model = Comment_photo
		fields = ['text']
		
class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['recipient', 'subject', 'body']

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['recipient'].queryset = User.objects.exclude(username=user.username)