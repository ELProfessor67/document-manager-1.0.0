from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from documents.models import Role, UserDetails

# def register(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         raw_password = request.POST.get('password')
#         craw_password = request.POST.get('cpassword')
#         email = request.POST.get('email')
#         role_id = request.POST.get('role')

#         if raw_password != craw_password:
#             return render(request, 'account/register.html', {'error_message': 'Password and confirm password does not match'})
        

#         if username and raw_password and email:
            
#             # Check if username is unique
#             if User.objects.filter(username=username).exists():
#                 return render(request, 'account/register.html', {'error_message': 'Username already exists'})

#             # Check if email is unique
#             if User.objects.filter(email=email).exists():
#                 return render(request, 'account/register.html', {'error_message': 'Email already exists'})
            
#             # Create user
#             user = User.objects.create_user(username=username, email=email, password=raw_password)

#             # Authenticate and login user
            
#             user = authenticate(username=username, password=raw_password)
#             login(request, user)

#             return redirect('/documents-uploads')  # Redirect to the homepage after successful registration
#         else:
#             return render(request, 'account/register.html', {'error_message': 'All fields are required'})

#     roles = Role.objects.all()
#     print(roles)
#     return render(request, 'account/register.html',{"roles": roles})


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        raw_password = request.POST.get('password')
        craw_password = request.POST.get('cpassword')
        email = request.POST.get('email')
        role_id = request.POST.get('role')

        if raw_password != craw_password:
            return render(request, 'account/register.html', {'error_message': 'Password and confirm password does not match'})

        if username and raw_password and email:
            # Check if username is unique
            if User.objects.filter(username=username).exists():
                return render(request, 'account/register.html', {'error_message': 'Username already exists'})

            # Check if email is unique
            if User.objects.filter(email=email).exists():
                return render(request, 'account/register.html', {'error_message': 'Email already exists'})
            
            # Create user
            user = User.objects.create_user(username=username, email=email, password=raw_password)

            # Create UserDetails instance
            role = Role.objects.get(pk=role_id)  # Assuming you have a Role model
            user_details = UserDetails.objects.create(user=user, role=role)

            # Authenticate and login user
            user = authenticate(username=username, password=raw_password)
            login(request, user)

            return redirect('/documents-uploads')  # Redirect to the homepage after successful registration
        else:
            return render(request, 'account/register.html', {'error_message': 'All fields are required'})

    roles = Role.objects.all()
    return render(request, 'account/register.html', {"roles": roles})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        if username and password:
            # Authenticate user
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if user.is_superuser:
                    return redirect('/dashboard')  # Redirect to the homepage after successful login
                else:
                    return redirect('/documents-lists')  # Redirect to the homepage after successful login
            else:
                return render(request, 'account/login.html', {'error_message': 'Invalid username or password'})

        else:
            return render(request, 'account/login.html', {'error_message': 'Username and password are required'})

    return render(request, 'account/login.html')

def logout_view(request):
    logout(request)
    # Redirect to a page after logout, for example, the home page
    return redirect('/')