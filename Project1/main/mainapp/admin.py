from django.contrib import admin
from .models import Event
from .models import readingMaterial, classList, Post, Profile
from .models import readingMaterial, classList, Post, Supply


# Register your models here. Basically written by copilot. I wrote the first 3 letters and it finished it for me
admin.site.register(Event) 
admin.site.register(readingMaterial)
admin.site.register(classList)
admin.site.register(Post)
admin.site.register(Profile)
admin.site.register(Supply)
