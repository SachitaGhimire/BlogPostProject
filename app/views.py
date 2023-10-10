from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from app.models import BlogPost, Profile, Comment
from django.db.models import Q
from .forms import UploadForm
import pandas as pd
from django.db import transaction
from .ml import get_recommendation_for_blog

def index(request):
    blog = BlogPost.objects.all().order_by('-id')
    paginator = Paginator(blog, 10)
    page_number = request.GET.get('page')
    pagefinal = paginator.get_page(page_number)
    return render(request, 'index.html',{'blog':pagefinal})


def register(request):
        if request.method == "POST":
            username = request.POST['username']
            email = request.POST['email']
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            password1 = request.POST['password1']
            password2 = request.POST['password2']

            if password1 != password2:
                messages.error(request, "Passwords do not match.")
                return redirect('/register')

            user = User.objects.create_user(username, email, password1)
            user.first_name = first_name
            user.last_name = last_name
            user.save()
            return redirect('signin')
        return render(request, 'register.html')

def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        print(username, password)
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect('/')
        else:
            messages.error(request, "Invalid Credentials")
            return redirect('signin')

    return render(request, 'login.html')

def out(request):
    logout(request)
    messages.success(request, 'Logout successfully')
    return redirect('signin')


def blogDeatils(request, id):
    blog = BlogPost.objects.get(id=id)
   
    p_ids = get_recommendation_for_blog(blog.id)
    print(p_ids)
    recommended_blog = BlogPost.objects.filter(id__in=p_ids).order_by('id')
    list_of_course = list(recommended_blog)
    print(list_of_course)
    
    # blog.save()
    comment = Comment.objects.filter(blog=BlogPost.objects.get(id=id))
    # if Profile.objects.filter(user=blog.user):
    #     p = Profile.objects.get(user=blog.user)
    #     return render(request, 'blogDetails.html', {'blog': blog, 'p': p,'c':comment})
    return render(request, 'blogDetails.html', {'blog': blog,'c':comment, 'recommend' : list_of_course})


def contact(request):
    return render(request,'contact.html')



def comment(request):
    if request.method == "POST":
        comment=request.POST['comment']
        id  =request.POST['id']
        comment = Comment(user= request.user,comment=comment,blog=BlogPost.objects.get(id=id))
        comment.save()
        messages.success(request, "comment successfully")
        return redirect(f'blogDetails/{id}')

def profile(request):
    u = User.objects.get(username=request.user)
    if Profile.objects.filter(user=request.user):
        p = Profile.objects.get(user=request.user)
        return render(request, 'profile.html', {'p': p, 'u': u})
    else:
        return render(request, 'profile.html', {'u': u})



def addProfile(request):
    if request.method == "POST":
        profile = Profile(user= request.user, image=request.FILES['image'])
        profile.save()
        return redirect('/profile')


def deleteComment(request, id):
    Comment.objects.filter(id=id).delete()
    blog_id = request.POST['blog_id']
    return  redirect(f'/blogDetails/{blog_id}')

def editComment(request, id):
    e = Comment.objects.get(id=id)
    blog_id = request.POST['blog_id']
    return render(request, 'editComment.html', {'e': e, 'blog_id': blog_id})

def updateComment(request, id):
    Comment.objects.filter(id=id).update(comment=request.POST['editedComment'])
    blog_id = request.POST['blog_id']
    return redirect(f'/blogDetails/{blog_id}')

def updateProfile(request):
    if request.method == "POST":
        profile = Profile.objects.get(user=request.user)
        profile.image = request.FILES['image']
        profile.save()
        return redirect('/profile')

def search(request):
    if request.method == "POST":
        search = request.POST['search']
        blog = BlogPost.objects.all().filter(
            Q(title__icontains=search) | Q(subtitle__icontains=search) | Q(content__icontains=search)
        )
        return render(request, 'search.html',{'blog':blog})

def upload_dataset(request):
        file_form = UploadForm()
        error_messages = {}

        if request.method == "POST":
            file_form = UploadForm(request.POST, request.FILES)
            try:
                if file_form.is_valid():
                    dataset = pd.read_csv(request.FILES['uploadfile'])
                    new_post = []
                
                   
                    with transaction.atomic():
                        for index, row in dataset.iterrows():
                            blog = BlogPost(
                                title=row['title'],
                                user_id=row['user'],
                                subtitle=row['subtitle'],
                                content=row['content'],
                                image=row['image'],
                            )

                            new_post.append(blog)

                    BlogPost.objects.bulk_create(new_post)
            except Exception as e:
                error_messages['error'] = e
      
        return render(request, 'upload_dataset.html', {'form': file_form, 'error_messages': error_messages})
