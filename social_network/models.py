from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nickname = models.CharField(max_length=100, blank=True)
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True)
    follow = models.ManyToManyField('self', blank=True, symmetrical=False)

    def __str__(self):
        return self.user.username


class Post(models.Model):
	title = models.CharField(max_length=100)
	text = models.TextField()
	user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='post_set')
	pub_date = models.DateTimeField('date published', auto_now_add=True)

	def __str__(self):
		return f'{self.title}'

class Comment_post(models.Model):
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	com_date = models.DateTimeField('date commented', auto_now_add=True)
	text = models.TextField()

	def __str__(self):
		return f'{self.text}'


class Photo(models.Model):
	user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='photo_set')
	title = models.CharField(max_length=100)
	pub_date = models.DateTimeField('date published', auto_now_add=True)
	picture = models.ImageField(upload_to='content/', blank=True)

	def __str__(self):
		return f'{self.title}'

class Comment_photo(models.Model):
	post = models.ForeignKey(Photo, on_delete=models.CASCADE)
	com_date = models.DateTimeField('date commented', auto_now_add=True)
	text = models.TextField()

	def __str__(self):
		return f'{self.text}'

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=200)
    body = models.TextField()
    sent_date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.subject