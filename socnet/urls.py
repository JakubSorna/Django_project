
from django.contrib import admin
from django.urls import path
from social_network import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.register, name='register'),
    path('login/', views.login_view, name='login_view'),
    path('logout/', views.logout_view, name= 'logout_view'),
    path('my_profile/', views.my_profile, name='my_profile'),
    path('setting/', views.setting, name='setting'),
    path('profile_setting/', views.set_profile, name='set_profile'),
    path('profile/<str:nickname>/', views.profile, name='profile'),
    path('search/', views.search, name='search'),
    path('livesearch/<str:word>/<int:sid1>.<int:sid2>', views.livesearch, name='livesearch'),
    path('add_post/', views.add_post, name='add_post'),
    path('add_photo/', views.add_photo, name= 'add_photo'),
    path('home/', views.home, name='home'),
    path('post_detail/<int:post_id>/', views.post_detail, name='post_detail'),
    path('photo_detail/<int:post_id>/', views.photo_detail, name='photo_detail'),
    path('send_message/', views.send_message, name='send_message'),
    path('inbox/', views.inbox, name='inbox'),
    path('read_message/<int:message_id>/', views.read_message, name='read_message'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
