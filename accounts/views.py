from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib import auth
from contacts.models import Contact

def register(request):
    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password_confirmation = request.POST['password_confirmation']

        #Check if passwords math
        if password == password_confirmation:
            #Check if username exists
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already taken!')
                return redirect('register')
            else:
                #Check if email exists
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'Email already taken!')
                    return redirect('register')
                else:
                    #If validation passed, create user and log him in
                    user = User.objects.create_user(
                        username=username,
                        password=password,
                        first_name=first_name,
                        last_name=last_name,
                        email=email
                    )
                    messages.success(request, 'Registration successful. You are now logged in')
                    auth.login(request, user)
                    return redirect('index')
        else:
            messages.error(request, 'Password confirmation didn\'t match!')
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)

        if(user is not None):
            auth.login(request, user)
            messages.success(request, 'Successfully logged in!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials. Try again!')
            return redirect('login')

        return redirect('login')
    else:
        return render(request, 'accounts/login.html')

def logout(request):
    auth.logout(request)
    return redirect('index')

def dashboard(request):
    user_contacts = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)
    context = {
        'contacts': user_contacts
    }
    return render(request, 'accounts/dashboard.html', context)