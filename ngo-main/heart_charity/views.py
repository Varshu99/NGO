from django.shortcuts import render, redirect
from .models import Volunteer, Contact, Cause,Donate
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.forms import ValidationError



# Create your views here.
# def base(request):
#     causes=Cause.objects.all()
#     return render(request,'base.html',{"causes":causes})
def home(req):
    return render(req,'home.html')
    
def logout_view(req):
    logout(req)
    return render(req,"home.html")

def submit_valunteer(request):
    if request.method =="POST":
        name=request.POST['name']
        email=request.POST['email']
        subject=request.POST['subject']
        message=request.POST.get('message')

        volunteer=Volunteer.objects.create(name=name,email=email,subject=subject,message=message)
        volunteer.save()
        return redirect('/')
    else:
        return redirect('/')

def contact(request):
    if request.method =="POST":
        f_name=request.POST['f_name']
        l_name=request.POST['l_name']
        email=request.POST['email']
        message=request.POST.get('message')

        contact=Contact.objects.create(name=f"{f_name}  {l_name}",email=email,message=message)
        contact.save()
        return redirect('/')
    else:
        return redirect('/')

@login_required(login_url=reverse_lazy("login"))
def donate(request,id):
    if request.method =="POST":
        name=request.POST['name']
        email=request.POST['email']
        amount=request.POST.get('amount')

        cause=Cause.objects.get(id=id)
        cause.raised=cause.raised+float(amount)
        cause.goal=cause.goal-float(amount)
        cause.save()
        donation=Donate.objects.create(name=name,email=email,amount=float(amount))
        donation.save()
        return redirect('/')
    else:
        cause=Cause.objects.get(id=id)
        return render(request,'donate.html',{"cause":cause})


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages

# def signup_view(request):
#     if request.method == 'POST':
#         username = request.POST['username']
#         email = request.POST['email']
#         password = request.POST['password']
#         if User.objects.filter(username=username).exists():
#             messages.error(request, 'Username already exists.')
#             return redirect('signup')
#         user = User.objects.create_user(username=username, email=email, password=password)
#         user.save()
#         messages.success(request, 'Account created successfully. Please log in.')
#         return redirect('signin')
#     return render(request, 'signup.html')


def signin_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')  # redirect to home or dashboard
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('signin')
    return render(request, 'signin.html')



def validate_password(password):
    # Check minimum length
    if len(password) < 8:
        raise ValidationError("Password must be at least 8 characters long.")

    # Check maximum length
    if len(password) > 128:
        raise ValidationError("Password cannot exceed 128 characters.")

    # Initialize flags for character checks
    has_upper = False
    has_lower = False
    has_digit = False
    has_special = False
    special_characters = "@$!%*?&"

    # Check for character variety
    for char in password:
        if char.isupper():
            has_upper = True
        elif char.islower():
            has_lower = True
        elif char.isdigit():
            has_digit = True
        elif char in special_characters:
            has_special = True

    if not has_upper:
        raise ValidationError("Password must contain at least one uppercase letter.")
    if not has_lower:
        raise ValidationError("Password must contain at least one lowercase letter.")
    if not has_digit:
        raise ValidationError("Password must contain at least one digit.")
    if not has_special:
        raise ValidationError(
            "Password must contain at least one special character (e.g., @$!%*?&)."
        )

    # Check against common passwords
    common_passwords = [
        "password",
        "123456",
        "qwerty",
        "abc123",
    ]  # Add more common passwords
    if password in common_passwords:
        raise ValidationError("This password is too common. Please choose another one.")



def signup_view(req):
    context = {}
    if req.method == "POST":
        username = req.POST["username"]
        email = req.POST["email"]
        password1 = req.POST["password1"]
        password2 = req.POST["password2"]

        try:
            validate_password(password1)
        except ValidationError as e:
            context["errmsg"] = str(e)
            return render(req, "signup.html", context) 

        if username == "" or password1 == "" or password2 == "":
            context["errmsg"] = "Field can't be empty"
            return render(req, "signup.html", context)

        elif password1 != password2:
            context["errmsg"] = "Password and confirm password doesn't match"
            return render(req, "signup.html", context)

        elif username.isdigit():
            context["errmsg"] = "Username can't be only number"
            return render(req, "signup.html", context)
            
        elif password1 == username:
            context["errmsg"] = "Password cannot same as username"
            return render(req, "signup.html", context)
        else:
            try:
                userdata = User.objects.create(username=username, password=password1)
                userdata.set_password(password1)
                userdata.save()
                print(User.objects.all())
                return redirect("signin")
            except:
                print("User already exists")
                context["errmsg"] = "User already exists"
                return render(req, "signup.html", context)

    return render(req, "signup.html")


def request_password_reset(req):
    if req.method == "GET":
        return render(req, "request_password_reset.html")
    else:
        uname = req.POST.get("uname")
        context = {}
        try:
            userdata = User.objects.get(username=uname)
            return redirect("reset_password", uname=userdata.username)

        except User.DoesNotExist:
            context["errmsg"] = "No account found with this username"
            return render(req, "request_password_reset.html",context)

def reset_password(req, uname):
    userdata = User.objects.get(username=uname)
    if req.method == "GET":
        return render(req, "reset_password.html", {"user": userdata.username})
    else:
        upass = req.POST["upass"]
        ucpass = req.POST["ucpass"]
        context = {}
        userdata = User.objects.get(username=uname)
        try:
            if upass == "" or ucpass == "":
                context["errmsg"] = "Field can't be empty"
                return render(req, "reset_password.html", context)
            elif upass != ucpass:
                context["errmsg"] = "Password and confirm password need to match"
                return render(req, "reset_password.html", context)
            else:
                # validate_password(upass)
                userdata.set_password(upass)
                userdata.save()
                return redirect("signin")

        except ValidationError as e:
            context["errmsg"] = str(e)
            return render(req, "reset_password.html", context)

def our_causes(req):
    
    return render(req,"our_causes.html")