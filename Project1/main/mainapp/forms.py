from django import forms
from django.forms.widgets import SelectDateWidget, TimeInput
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

from .models import Event, readingMaterial, classList, Profile, supplyItem
# I got a lot of use from this https://docs.djangoproject.com/en/5.0/ref/forms/widgets/
#https://www.geeksforgeeks.org/django-form-field-custom-widgets/
#https://cdf.9vo.lt/3.0/django.forms.widgets/SelectDateWidget.html

# User / Profile stuff
# https://docs.djangoproject.com/en/5.0/topics/signals/ signals for the User to Profile transfer
# https://www.devhandbook.com/django/user-profile/

# Wes -- written in large part by copilot
class EventForm(forms.ModelForm):
    """
    A form for creating or updating an event.

    Fields:
    - title: CharField - The title of the event.
    - description: Textarea - The description of the event.
    - date: DateField - The date of the event.
    - time: TimeField - The time of the event.

    Usage:
    form = EventForm()
    """
    title = forms.CharField(label='Title', max_length=100)
    description = forms.Textarea()
    #todo by should allow the user to select a date and time
    # Got help from here https://stackoverflow.com/questions/72627164/django-datetime-typeerror-fromisoformat-argument-must-be-str
    url = forms.URLField(label='URL', required=False)
    date = forms.DateField(widget=SelectDateWidget())
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    class Meta:                                                                     # and here https://docs.djangoproject.com/en/3.0/ref/forms/widgets/#selectdatewidget
        model = Event
        fields = ['title', 'description','url', 'date', 'time']

class ReadingMaterialForm(forms.ModelForm):
    """
    A form for creating or updating a reading material.

    Attributes:
        title (str): The title of the reading material.
        author (str): The author of the reading material.
        type (str): The type or category of the reading material.
        link (str): The link to the reading material.

    """
    class Meta:
        model = readingMaterial
        fields = ['title']

class SupplyItemForm(forms.ModelForm):
    """
    A form for creating or updating supplies.

    Attributes:
        name (str): The title of the supply.
        link (str): Link to buy supply.
        purchased (bool): Indicates whether the supply material has been purchased or not.


    """
    class Meta:
        model = supplyItem
        fields = ['name', 'link', 'purchased']
        
        
# Wes -- Create a form to add a class

class classListForm(forms.ModelForm):
    """
    A form for creating or updating a class.

    Attributes:
        title (str): The title of the class.
        description (str): The description of the class.
        attributes (str): The attributes of the class. Theory, applications, ect
        time (str): The time of the class.
        date (str): The dates of the class, Aka monday, wednesday, friday
    """
    model = classList
    title = forms.CharField(label='Title', max_length=100)
    description = forms.Textarea()
    attributes = forms.CharField(label='Attributes', max_length=100)
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), required=False)
    date = forms.CharField(label='Date', max_length=100, required=False)
    
    currently_taking = forms.BooleanField(label='Currently Taking', required=False)
    completed = forms.BooleanField(label='Completed', required=False)
    

    class Meta:
        model = classList
        fields = ['title', 'description', 'attributes', 'time', 'date', 'currently_taking', 'completed']
        widgets = {
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'currently_taking': forms.CheckboxInput(),
            'completed': forms.CheckboxInput(),
    }



# Create a form to register a user
class RegistrationForm(UserCreationForm):
    """
    A form for user registration.

    Inherits from UserCreationForm and adds an email field.
    """

    email = forms.EmailField(required=True) #enforce email requirement

    class Meta: # https://docs.djangoproject.com/en/3.0/topics/auth/default/
        model = User 
        fields = ('username', 'email', 'password1', 'password2') #fields to be filled out by the user

    def save(self, commit=True): #save the user
        user = super(RegistrationForm, self).save(commit=False) #save the user
        user.email = self.cleaned_data['email'] #get the email
        if commit: #if the user is committed
            user.save() #save the user
        return user #return the user
    

class UserUpdateForm(forms.ModelForm):
    """
    A form for updating user information.

    This form allows users to update their username and email address.

    Attributes:
        email (EmailField): The email field for the user's email address.

    Meta:
        model (User): The User model to be used for the form.
        fields (list): The fields to be included in the form.

    """
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']


class UserForm(forms.ModelForm):
    """
    A form for updating user profile information.

    This form is used to update the first name, last name, and email fields of a user.

    Attributes:
        model (User): The User model to be used for the form.
        fields (list): The list of fields to be included in the form.

    """
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class ProfileUpdateForm(forms.ModelForm):
    """
    A form for updating the user profile.

    This form is used to update the user's bio, profile picture, location, and pets.

    Attributes:
        bio (str): The user's biography.
        profile_picture (str): The URL of the user's profile picture.
        location (str): The user's location.
        pets (str): The user's pets.
        interests (str): The user's interests.
        user_years (str): current student status.

    """
    class Meta:
        model = Profile
        fields = ['bio', 'profile_picture', 'location', 'pets', 'interests', 'user_years']
