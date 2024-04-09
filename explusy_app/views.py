from django.shortcuts import render,redirect #for rendering templates
from django.http import HttpResponse  #for getting response from the server
from django.contrib.auth.models import User, auth  
from django.contrib import messages
from .models import Profile
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required(login_url='signin') #This locks the homepage redirects to signin page
def index(request):
    user_object=User.objects.get(username=request.user)
    user_profile=Profile.objects.get(user=user_object)
    return render(request,'index.html',{'user_profile':user_profile })

def signup(request):
    #post is when all the data entered is checked
    
    if request.method =='POST':
        username=request.POST['username']
        email=request.POST['email']
        password=request.POST['password']
        password2=request.POST['password2']
        
        if password==password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,'email already exists')    #checking if email already exists
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request,'The user name already exists')
                return redirect(signup)
            else:
                user=User.objects.create_user(username=username,email=email,password=password)
                user.save()
                #login user an redirect to settings page
                user_login=auth.authenticate(username=username,password=password)
                auth.login(request,user_login)
                #create aprofile object for the new user
                user_model=User.objects.get(username=username)
                new_profile=Profile.objects.create(user=user_model,id_user=user_model.id)
                new_profile.save()
                return redirect('setting')
        else:
            messages.info(request,'Password not matching')  #for error message
            return redirect('signup')
            
        
        
    else:
        return render(request,'signup.html')
    
def signin(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        #user authentication
        user=auth.authenticate(username=username,password=password) 
        
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        #this else block gives an error message if the user's account is unavailable
        else:
            messages.info(request,'Account is not found')
            return redirect('signin')
        
    else:
        return render(request,'signin.html')
    
    
@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')

    
@login_required(login_url='signin') 
def setting(request):
    user_profile=Profile.objects.get(user=request.user)

    if request.method=='POST':
        #checks if any picture is uploaded and gets all information
        if request.FILES.get('image')==None:
            image=user_profile.profileimg
            bio=request.POST['bio']
            location=request.POST['location']
            
            user_profile.profileimg=image
            user_profile.bio=bio
            user_profile.location=location
            user_profile.save()
            
        if request.FILES.get('image')!=None:
            image=request.FILES.get('image')
            image=user_profile.profileimg
            bio=request.POST['bio']
            location=request.POST['location']
            
            user_profile.profileimg=image
            user_profile.bio=bio
            user_profile.location=location
            user_profile.save()
            
        return redirect('setting')
            

    return render(request,'setting.html',{'user_profile':user_profile})
    

@login_required(login_url='signin')
def upload(request):
    return HttpResponse("<h1>upload view</h1>")
    