from calendar import monthrange
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.utils import timezone
from django.db.models import Q
from .forms import EventForm, ReadingMaterialForm, ReadingMaterialForm, classListForm
from .models import Event, readingMaterial, classList, Post, Supply
from django.urls import reverse
from datetime import date, timedelta
from django.shortcuts import render
from datetime import date, timedelta
from calendar import monthcalendar, monthrange
from datetime import timedelta
import calendar
import os
import random
from django.conf import settings
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
import os
import random
from django.conf import settings

from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth import logout
from .forms import RegistrationForm # import the RegistrationForm class from forms.py
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, ProfileUpdateForm, UserForm, Profile # import the UserUpdateForm and ProfileUpdateForm classes from forms.py
from django.contrib import messages 
from django.contrib.auth.models import User


# https://openclassrooms.com/en/courses/7107341-intermediate-django/7264297-create-an-image-upload-facility

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
    user = request.user
    if not user.is_authenticated:
        return redirect('login') # Redirect to the login page by default CHANGE LATER OR UPDATE NAVBAR 
    else:
        return render(request, 'registration/profile.html', {'user': user})

# Seamus 
# repurposed the reading material view to function as the 'onboarding checklist' view
# not renamed due to complications on with django migrations 
def reading_material_view(request): 
    form = ReadingMaterialForm() # Create a new form object
    confetti = False # Set the confetti flag to False by default
    if request.method == 'POST': 
        form_type = request.POST.get('form_type') # Get the form type from the POST data
        if form_type == 'add':
            form = ReadingMaterialForm(request.POST) # Create a new form object with the POST data
            if form.is_valid():
                form.save() # Save the form data to the database
            else: # If the form is not valid, create a new form object
                form = ReadingMaterialForm() # Create a new form object
        elif form_type == 'update': # If the form type is 'update'
            user = request.user # Get the currently logged-in user
            item_id = request.POST.get('item_id') # Get the ID of the reading material item
            item = readingMaterial.objects.get(id=item_id) # Get the reading material item from the database

            # Update the read status and check if it's being set to True
            if 'read' in request.POST and not item.read:
                confetti = True  # Set the confetti flag

            item.read = 'read' in request.POST # Update the read status
            item.save() # Save the changes to the database

            # Badge logic
            if item.title == 'Visited the faculty page': # If the item is 'Visited the faculty page'
                user.profile.facultyBadge = True # Set the faculty badge to True
                user.profile.badgeScore += 1 
            elif item.title == 'Visited the events page':
                user.profile.eventsBadge = True
            elif item.title == 'Visited the HAM page':
                user.profile.hamBadge = True
            elif item.title == 'Visited the dorm page':
                user.profile.dormBadge = True
            elif item.title == 'Picked classes and added them to the calendar':
                user.profile.classBadge = True
            user.profile.save()

            item.read = 'read' in request.POST
            item.save()
        elif form_type == 'clear': 
            readingMaterial.objects.filter(read=True).delete()

    reading_list = readingMaterial.objects.all() # Get all the reading material items from the database
    context = { # Create the context dictionary
        'form': form,
        'reading_list': reading_list,
        'show_confetti': confetti
    }
    return render(request, 'readingList.html', context) # Render the readingList.html template with the context dictionary

# Lainey: gpt wrote most of this, but it is also very similar to Safari's reading list

def supplies_list(request):
    supplies = Supply.objects.all()
    return render(request, 'supplies.html', {'supplies': supplies})



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
    user = request.user

    today = date.today()

    if request.method == 'POST':
        form = EventForm(request.POST)
        if form.is_valid():
            event = form.save(commit=False) # trying to connect events with users
            event.user = user  # Associate the new event with the currently logged-in user
            event.save()
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
            events = Event.objects.filter(date=day_date, user=user) # Get the events for the day
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
                        events = Event.objects.filter(date=day_date, user=user)
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

#Seamus
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

#Seamus
def register(request):
    """
    Register a user.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object.

    """
    if request.method == 'POST': # if the user is trying to register
        form = RegistrationForm(request.POST) # get the form
        if form.is_valid(): # if the form is valid
            user = form.save() # save the user
            auth_login(request, user) # log the user in 
            return redirect('profile')  # redirect to the profile page
    else:
        form = RegistrationForm() # if the form is not valid, create a new form
    return render(request, 'registration/register.html', {'form': form}) # render the register page with the form

#Seamus
@login_required  # Ensures only logged-in users can access this view
def profile(request):
    """
    View function to display user profile.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object.

    """
    if request.method == 'POST': # if the user is trying to update their profile
        u_form = UserUpdateForm(request.POST, instance=request.user) # get the user form
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile) # get the profile form

        if u_form.is_valid() and p_form.is_valid(): # if the forms are valid
            u_form.save()
            p_form.save() # save the forms
            messages.success(request, f'Your account has been updated!')
            return redirect('profile') # redirect to the profile page

    else: # if the user is not trying to update their profile
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile) # get the user and profile forms

    return render(request, 'registration/profile.html', {'user': request.user}) # render the profile page with the user form

#Seamus
@login_required
def update_profile_picture(request):
    """
    View function to update the user's profile picture.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponseRedirect: Redirects to the 'profile' view.

    Raises:
        None
    """
    if request.method == 'POST': # if the user is trying to update their profile picture
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile) # get the profile form
        if form.is_valid(): # if the form is valid
            form.save() # save the form
            messages.success(request, 'Your profile picture has been updated!') # display a success message
            return redirect('profile') # redirect to the profile page
        else: # if the form is not valid
            messages.error(request, 'Unable to update your profile picture.') # display an error message
    return redirect('profile') # redirect to the profile page

#Seamus
@login_required
def edit_profile(request):
    """
    View function to edit the user's profile.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The HTTP response object.

    """
    if request.method == 'POST': # if the user is trying to edit their profile
        user_form = UserForm(request.POST, instance=request.user)  # get the user form
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile) # get the profile form

        if user_form.is_valid() and profile_form.is_valid(): # if the forms are valid
            user_form.save()
            profile_form.save() # save the forms
            messages.success(request, 'Your profile has been updated!') # display a success message
            return redirect('profile')  # redirect to the profile page
    else: # if the user is not trying to edit their profile
        user_form = UserForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile) # get the user and profile forms

    context = { # create the context dictionary
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'registration/editProfile.html', context) # render the editProfile page with the context dictionary

#Seamus
@login_required
def logout_view(request):
    """
    Logs out the current user and redirects to the home page.

    Args:
        request: The HTTP request object.

    Returns:
        A redirect response to the home page.
    """
    logout(request) # log the user out
    return redirect('home') # redirect to the home page


# Bilge
@login_required
def dorms(request):
    return render(request, "dorms.html")

#Lainey
def eateries(request):
    return render(request, 'eateries.html', {})

def local_fun(request):
    return render(request, 'local_fun.html', {})

def transportation(request):
    return render(request, 'transportation.html', {})

def food_art(request):
    return render(request, 'food_art.html', {})

def groceries_supplies(request):
    return render(request, 'groceries_supplies.html', {})

def catalyst(request):
    embed_url = 'https://ncfcatalyst.com/'
    return render(request, 'catalyst.html', {'embed_url': embed_url})

def supplies(request):
    return render(request, 'supplies.html', {})
# Bilge
@login_required
def conovo(request):
    if request.method == "POST":
        if "conovoSubmit" in request.POST:
            content = request.POST.get('content', '').strip() # get the post submitted by user
            if 1:  # TO-DO: Ensure the description is not empty
                Post.objects.create(content=content, author=request.user) # save the task in the database with name
                messages.success(request, "Message Posted! Slay! 🌊 ")
                return redirect('conovo')
            else: #TO-DO to return a message to enter a valid post submission
                return render(request, "conovo.html")
    else: # if the method is GET
        # Query the Post objects including related User objects (authors)
        posts = Post.objects.select_related('author').all()
        leaderlist = leaderboard()
        return render(request, 'conovo.html', {'posts': posts, "top3": leaderlist[:3], "top4_10": leaderlist[4:]})

#bilge
@login_required
def other_profile(request, author):
    user = User.objects.get(username=author)
    return render(request, 'other_profile.html', {'user': user} )


def leaderboard():
    leaderlist = Profile.objects.all().order_by('-badgeScore')[:10]
    return leaderlist