from django.shortcuts import render, HttpResponse, redirect
from .models import Contact
from django.contrib import messages
from blog.models import Post
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

# HTML pages
def home(request):
    # return HttpResponse('This is home')
    # Fetch top three posts based on number of views?
    
    allPosts = Post.objects.all()
    print(allPosts)
    context = {'allPosts': allPosts}
    return render(request, 'home/home.html', context)

def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        content = request.POST['content']

        if(len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<4):
            messages.error(request, 'Please fill the form correctly!')
        else:
            contact = Contact(name=name, email=email, phone=phone, content=content)
            contact.save()
            messages.success(request, 'Your message has been send successfully!')

    return render(request, 'home/contact.html')

def about(request):
    return render(request, 'home/about.html')

def search(request):
    query = request.GET['query']
    if len(query) > 78:
        # allPosts = [] OR
        allPosts = Post.objects.none()
    else:
        # allPosts = Post.objects.all()
        allPostsTitle = Post.objects.filter(title__icontains=query)
        allPostsContent = Post.objects.filter(content__icontains=query)
        allPosts = allPostsTitle.union(allPostsContent)
    if allPosts.count() == 0:
        messages.warning(request, "No search results found. Please refine your query!")
    params = {'allPosts': allPosts, 'query': query}
    return render(request, 'home/search.html', params)
    # return HttpResponse('This is search')


# Authentication APIs
def handleSignup(request):
    if request.method == 'POST':
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # Check for errorneous inputs
        if len(username) > 10:
            messages.error(request, 'Username must be at least 10 characters')
            return redirect('home')
        
        if not username.isalnum(): #isalnum() allows alphabetic and numeric characters together
            messages.error(request, 'please enter a valid username')
            return redirect('home')
        
        if pass1 != pass2:
            messages.error(request, 'Passwords do not match')
            return redirect('home')
        


        # Create the user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request, 'Your iCoder account has been created successfully!')
        return redirect('home')
    else:
        return HttpResponse('404 - Not Found')
    

def handleLogout(request):
    logout(request)
    messages.success(request, 'User has been logged out')
    return redirect('home')
    

def handleLogin(request):
    if request.method == 'POST':
        loginusername = request.POST['loginusername']
        loginpass = request.POST['loginpass']

        user = authenticate(username=loginusername, password=loginpass)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Invalid credentials, Please try again!')
            return redirect('home')
        
    return HttpResponse('404 - Not Found!')