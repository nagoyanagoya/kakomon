from django.contrib import admin
from .models import ProfileModel, SubjectModel, ImageModel

# Register your models here.
admin.site.register(ProfileModel)
admin.site.register(SubjectModel)
admin.site.register(ImageModel)
