from django import forms
from django.forms.widgets import SelectDateWidget, TimeInput

from .models import Event, readingMaterial, classList
# I got a lot of use from this https://docs.djangoproject.com/en/5.0/ref/forms/widgets/
#https://www.geeksforgeeks.org/django-form-field-custom-widgets/
#https://cdf.9vo.lt/3.0/django.forms.widgets/SelectDateWidget.html

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
        fields = ['title', 'author', 'type', 'link']
        
        
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

        
        