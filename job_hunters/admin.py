from django.contrib import admin
from .models import (
    UserProfile,
    Application,
    Category,
    CompanyProfile,
    Image,
    Job,
    Experience,
    Recommendation,
)

# Register your models here.

admin.site.register(UserProfile)
admin.site.register(Application)
admin.site.register(Category)
admin.site.register(CompanyProfile)
admin.site.register(Image)
admin.site.register(Job)
admin.site.register(Experience)
admin.site.register(Recommendation)
