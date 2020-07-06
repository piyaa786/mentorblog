from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth.models import auth,User
from PIL import Image
from django.utils.timezone import now

#from embed_video.fields import EmbedVideoField


# user profile
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='profile_pic',null=True,default='default.jpg')
    dob = models.DateTimeField(null=True)
    bio = models.CharField(max_length=225)
    city = models.CharField(max_length=225)




# blog
class Blog(models.Model):
    title = models.CharField(max_length=130)
    image = models.ImageField(upload_to='post_images',blank = True)
    pdf = models.FileField(upload_to='post_pdf',blank = True)
    video = models.FileField(upload_to='videos',blank = True)
    content = models.TextField()
    teacher = models.CharField(max_length=130)
    technology =  models.CharField(max_length=130)
    liked = models.ManyToManyField(User, default=None,blank=True,related_name='liked')
    timestamp = models.DateTimeField(blank=True)

    def __str__(self):
        return self.title +   'by'    + self.teacher


    @property
    def num_likes(self):
        return self.liked.all.count()

LIKE_CHOICE= (
    ('Like','Like'),
    ('Unlike','Unlike'),
)

class Like(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Blog,on_delete=models.CASCADE)
    value = models.CharField(choices=LIKE_CHOICE, default='Like',max_length=10)

    def __str__(self):
        return str(self.post)
#postcomment
class PostComment(models.Model):
    sno = models.AutoField(primary_key = True)
    comment=models.TextField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    post = models.ForeignKey(Blog,on_delete=models.CASCADE)
    parent = models.ForeignKey('self',on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(default=now)




#assignments
class Assignment(models.Model):
    title = models.CharField(max_length=225)
    pdf = models.FileField(upload_to='assign_pdf',blank = True)
    content = models.TextField()
    teacher = models.CharField(max_length=225)
    technology =  models.CharField(max_length=130)
    timestamp = models.DateTimeField(blank=True)

    def __str__(self):
        return self.title +   'by'    + self.teacher

# submit assignments
class UploadAssignment(models.Model):
    title = models.ForeignKey(Assignment,on_delete=models.CASCADE)
    username = models.CharField(max_length=225)
    pdf = models.FileField(upload_to='pdf')

    def __str__(self):
        return self.titlee

class Feedback(models.Model):
    name = models.CharField(max_length=225)
    email = models.CharField(max_length=100)
    content = models.TextField()

    def __str__(self):
        return 'Feedback from' + ' ' + self.name
