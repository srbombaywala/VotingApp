from django.contrib import admin
from .models import member

class UserDetailAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'picture', 'ppan', 'otp', 'has_voted','vote_casted')

# Register your model with the custom admin class
admin.site.register(member, UserDetailAdmin)
