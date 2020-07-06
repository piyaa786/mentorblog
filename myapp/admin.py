from django.contrib import admin
from myapp.models import UserProfile
from myapp.models import Blog,Like, Assignment,UploadAssignment,PostComment,Feedback

# Register your models here.


admin.site.register(UserProfile)
admin.site.register((Blog,PostComment))

admin.site.register(UploadAssignment)
admin.site.register(Like)

admin.site.register(Assignment)
admin.site.register(Feedback)






















