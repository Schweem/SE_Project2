from calendar import monthrange
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.db.models import Q
from .forms import EventForm, ReadingMaterialForm, ReadingMaterialForm, classListForm
from .models import Event, readingMaterial, classList
from datetime import date, timedelta
from django.shortcuts import render
from datetime import date, timedelta
from calendar import monthcalendar, monthrange
from datetime import timedelta
import calendar
import os
import random
from django.conf import settings
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
import os
import random
from django.conf import settings

from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from .forms import RegistrationForm # import the RegistrationForm class from forms.py
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm, UserForm, Profile # import the UserUpdateForm and ProfileUpdateForm classes from forms.py
from django.contrib import messages 

# I got a lot of help from here 
#https://www.w3schools.com/django
#and a lot of help from copilot

#todo list view by Wes
def todo_list(request): # copilot
    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('todo_list')
    else:
        form = EventForm()
    # Get the current date and time
    now = timezone.now()

    # Filter the todos to only include (uncompleted events and events in the past) or (completed events and events in the future)
    todos = Event.objects.filter(
        Q(completed=False, date__lte=now.date()) | 
        Q(date__gte=now.date())
    ).order_by('date', 'time')
    return render(request, 'todo_list.html', {'todos': todos, 'form': form})
# Wes
def delete_todo(request, todo_id): #copilot wrote this mostly 
    todo = get_object_or_404(Event, id=todo_id)
    todo.delete()
    return redirect('todo_list')

# identical to the delete_todo function but we just mark the todo as completed instead of deleting it. 
def mark_todo_completed(request, todo_id): # Wes
    todo = get_object_or_404(Event, id=todo_id)
    todo.completed = True
    todo.save()
    return redirect('todo_list')

def event_detail(request, event_id): # Wes
    event = get_object_or_404(Event, pk=event_id)
    return render(request, 'event_detail.html', {'event': event})
  
def home(request):
    return redirect('login') # Redirect to the login page by default CHANGE LATER OR UPDATE NAVBAR 

def reading_material_view(request): 
    form = ReadingMaterialForm()
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        if form_type == 'add':
            form = ReadingMaterialForm(request.POST)
            if form.is_valid():
                form.save()
            else:
                form = ReadingMaterialForm()
        elif form_type == 'update':
            item_id = request.POST.get('item_id')
            item = readingMaterial.objects.get(id=item_id)
            item.read = 'read' in request.POST
            item.save()
        elif form_type == 'clear':
            readingMaterial.objects.filter(read=True).delete()

    reading_list = readingMaterial.objects.all()
    return render(request, 'readingList.html', {'form': form, 'reading_list': reading_list})


#Safari -- Copilot wrote this -- Super simple
#View function to display our timer page
def pomodoro_timer(request):
    return render(request, 'timer.html')

#Safari -- Copilot wrote this 
#View function to display our draw page
def draw_view(request):
    return render(request, 'draw.html')

# Wes -- Generated by GPT 
def add_months(source_date, months): 
    month = source_date.month - 1 + months
    year = source_date.year + month // 12
    month = month % 12 + 1
    return date(year, month, 1)
# Wes -- Written by copilot and GPT over several iterations
def calendar_view(request, period):
    today = date.today()

    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('calendar', period=period)  # Adjust the redirect as needed
    else:
        form = EventForm()

    months_with_weeks = {}
    # if the persiod is a wee
    if period == 'week':
        start_week = today - timedelta(days=today.weekday()) # Get the first day of the week
        week_name = f"Week of {start_week.strftime('%B %d, %Y')}" # Generate the week's name
        week_days = []  # This will hold the days of the week
        for i in range(7): # Generate the data for each day in the week
            day_date = start_week + timedelta(days=i)   # Get the date of the day
            events = Event.objects.filter(date=day_date) # Get the events for the day
            # Append each day's data directly into the week_days list
            week_days.append({'day': day_date.day, 'events': events}) 
        # Now, week_days is a single list representing one week, as expected by the template
        months_with_weeks[week_name] = [week_days]  # Wrap week_days in a list to match the expected structure

    # Handle month and semester views
    elif period in ['month', 'semester']:
        months_to_generate = 1 if period == 'month' else 6
        start_month = today.replace(day=1)
        # Generate the data for each month
        for i in range(months_to_generate):
            month_date = add_months(start_month, i)
            month_name = calendar.month_name[month_date.month] + " " + str(month_date.year)
            month_days = monthcalendar(month_date.year, month_date.month)
            weeks = []
            # Move on to each individual week
            for week in month_days:
                week_days = []
                # Move on to each day in the week
                for day in week:
                    if day != 0: # If it's a day in the current month
                        day_date = date(month_date.year, month_date.month, day)
                        events = Event.objects.filter(date=day_date)
                        day_info = {'day': day, 'events': events}
                    else:
                        day_info = None
                    week_days.append(day_info) # Append the day's data to the week
                weeks.append(week_days)
            months_with_weeks[month_name] = weeks

    return render(request, 'calendar.html', {'months_with_weeks': months_with_weeks, 'form': form})

#Safari -- Copilot helped write this one as well

# View function for displaying memes
def memes(request):
    images_dir = os.path.join('mainapp', 'static', 'images')
    image_files = os.listdir(images_dir)
    random_image = random.choice(image_files)
    context = {
        'random_image': random_image
    }
    return render(request, 'memes.html', context)


# Wes -- Class List view written by copilot
def class_list_view(request): #copilot
    if(request.method == 'POST'):
        form = classListForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('class_list')
    else:
        form = classListForm()
    
    current_classes = classList.objects.filter(currently_taking=True, completed=False)
    completed_classes = classList.objects.filter(completed=True, currently_taking = False)
    future_classes = classList.objects.filter(currently_taking=False, completed=False)
    
    return render(request, 'class_list.html', {'current_classes': current_classes, 'completed_classes': completed_classes, 'future_classes': future_classes, 'form': form})

# Wes -- written by copilot
def delete_class(request, class_id): #copilot
    class_to_delete = get_object_or_404(classList, id=class_id)
    class_to_delete.delete()
    return redirect('class_list')

def hours(request):
    return render(request, 'hours.html')

## PROJECT 2 USER AUTH ## 

def login_view(request):  
    if request.method == 'POST': # if the user is trying to log in
        form = AuthenticationForm(request, data=request.POST) # get the form
        if form.is_valid(): # if the form is valid
            username = form.cleaned_data.get('username') # get the username
            password = form.cleaned_data.get('password') # get the password
            user = authenticate(request, username=username, password=password) # authenticate the user
            if user is not None:
                auth_login(request, user)  # pass 'user' to the login function
                return redirect('profile')  # redirect to the profile page
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def register(request): # user registration
    if request.method == 'POST': # if the user is trying to register
        form = RegistrationForm(request.POST) # get the form
        if form.is_valid(): # if the form is valid
            user = form.save() # save the user
            auth_login(request, user) # log the user in 
            return redirect('profile')  # redirect to the profile page
    else:
        form = RegistrationForm() # if the form is not valid, create a new form
    return render(request, 'registration/register.html', {'form': form}) # render the register page with the form

@login_required  # Ensures only logged-in users can access this view
def profile(request): # view to display user profile
    if request.method == 'POST': # if the user is trying to update their profile
        u_form = UserUpdateForm(request.POST, instance=request.user) # get the user form
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile) # get the profile form

        if u_form.is_valid() and p_form.is_valid(): # if the forms are valid
            u_form.save() # save the user form
            p_form.save() # save the profile form
            messages.success(request, f'Your account has been updated!') # success message
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }
    return render(request, 'registration/profile.html', {'user': request.user}) # render the profile page with the user's information

@login_required
def update_profile_picture(request): # view to update the user's profile picture
    if request.method == 'POST': # if the user is trying to update their profile picture
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile) # get the form
        if form.is_valid(): # if the form is valid
            form.save() # save the form
            #success message
            messages.success(request, 'Your profile picture has been updated!')
            return redirect('profile')  # Replace 'profile' with the name of your profile view
        else:
            # error message
            messages.error(request, 'Unable to update your profile picture.')
    # If GET or form not valid, render the profile page with the form
    return redirect('profile')

@login_required
def update_profile(request): # view to update the user's profile
    if request.method == 'POST': # if the user is trying to update their profile
        user_form = UserForm(request.POST, instance=request.user) # get the user form
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile) # get the profile form

        if user_form.is_valid() and profile_form.is_valid(): # if the forms are valid
            user_form.save() # save the user form
            profile = profile_form.save(commit=False) # save the profile form
            profile.user = request.user # set the profile's user to the current user
            profile.save() # save the profile form
            messages.success(request, 'Your profile has been updated!') # success message
            return redirect('profile')  
    else:
        user_form = UserForm(instance=request.user) # if the form is not valid, create a new form
        profile_form = ProfileUpdateForm(instance=request.user.profile) # if the form is not valid, create a new form

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'edit_profile.html', context)

@login_required
def edit_profile(request): # view to edit the user's profile
    if request.method == 'POST': # if the user is trying to edit their profile
        user_form = UserForm(request.POST, instance=request.user) 
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile) # Get the user and profile forms from the request
        
        if user_form.is_valid() and profile_form.is_valid(): # If the forms are valid
            user_form.save() # Save the user form
            profile_form.save() # Save the profile form
            messages.success(request, 'Your profile has been updated!')
            return redirect('profile')  # Redirect to the profile detail view after save
    else:
        user_form = UserForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'registration/editProfile.html', context)