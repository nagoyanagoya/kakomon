from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
# Create your models here.
class ProfileManager(models.Manager):
    def create_profile(self, user):
        profile = self.create(user=user)

class ProfileModel(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=500, blank=True)
    objects = ProfileManager()

class SubjectModel(models.Model):
    name = models.CharField(max_length=20)
    member = models.CharField(max_length=1000, blank=True)
    day = models.CharField(max_length=5,blank=True)

class ImageModel(models.Model):
    subject = models.ForeignKey(SubjectModel, on_delete = models.CASCADE)
    image= models.FileField(upload_to='')
    year = models.CharField(max_length=4)
    page = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    author = models.CharField(max_length=10,blank=True)
    when = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(2)])