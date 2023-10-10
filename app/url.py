from app import views
from django.urls import include, path

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('signin', views.signin, name='signin'),
    path('logout', views.out),
    path('blogDetails/<int:id>', views.blogDeatils),
    path('contact',views.contact),
    path('comment', views.comment, name='comment'),
    path('profile',views.profile),
    path('addProfile', views.addProfile),
    path('deleteComment/<int:id>', views.deleteComment),
    path('editComment/<int:id>', views.editComment),
    path('updateComment/<int:id>', views.updateComment),
    path('updateProfile', views.updateProfile),
    path('search', views.search),
    path('uploaddataset/', views.upload_dataset),

]