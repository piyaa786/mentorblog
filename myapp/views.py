
from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, redirect,get_object_or_404
from django.views.generic import View, DetailView, ListView
from django.contrib.auth.models import auth,User
from django.contrib.auth import login

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_text,DjangoUnicodeDecodeError

from django.core.mail import EmailMessage, send_mail
from django.conf import settings
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth import login as auth_login


from .models import UserProfile,  Assignment, Like
from django.contrib.auth.decorators import login_required

from  .models import Blog,UserProfile

from .form import UserUpdate, ProfileUpdate, UploadAssign
from  .models import UploadAssignment,PostComment,Feedback
from django.contrib import messages

from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from .templatetags import extras
from django.urls import reverse
# Create your views here.

def index(request):
    return render(request,'index.html')




def login(request):
    if request.method == 'POST':
        un = request.POST['usename']
        pass1 = request.POST['pass']

        user = auth.authenticate(username=un,password=pass1)
        if user is not None and user.is_active:
            auth.login(request,user)
            return redirect('/index')
        else:
            messages.info(request,'Invalid credentials')
            return redirect('/login')

    else:
        return render(request,'login.html')
def logout(request):
    auth.logout(request)
    return redirect('/index')

def Register(request):
    if request.method == 'POST':
        fn = request.POST['fname']
        ln = request.POST['lname']
        em = request.POST['email']
        un = request.POST['usname']
        pass1 = request.POST['pass']
        pass2 = request.POST['pass2']


        if not un.isalnum():
                print("ko")
                messages.info(request,"Username must be only contain letters and numbers")
                return redirect('/register')


        if pass1 == pass2:

            if User.objects.filter(username=un).exists():
                messages.info(request,'Username already Taken')
                print("Username Taken")
                return redirect('/register')
            elif User.objects.filter(email=em).exists():
                messages.info(request, "Email Taken")
                # print("Username Taken")
                return redirect('/register')
            else:
                user = User.objects.create_user(username=un, email=em, password=pass1, first_name=fn, last_name=ln)

                user.is_active=False

                user.save()
                UserProfile.objects.create(user=user)
                messages.info(request, 'wait until admin will not apprrove you !')

        else:
            print('password not matched !')
            messages.info(request, 'register')
        return redirect('/register')
    else:
        return render(request,"register.html")



# userprofile
@login_required
def edit_profile(request):
    if request.method=='POST':
        u_form = UserUpdate(request.POST,instance=request.user)
        p_form =  ProfileUpdate(request.POST,request.FILES,instance=request.user.userprofile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,'your profile is updated successfully')
    else:
        u_form = UserUpdate(instance=request.user)
        p_form =  ProfileUpdate(instance=request.user.userprofile)

    return render(request,'editprofile.html',{'u_form':u_form,'p_form':p_form})
#view user profile
@login_required
def view_profile(request):
    return render(request,'viewprofile.html')
def team(request):
    return render(request,'team.html')
def aboutus(request):
    return render(request,'aboutus.html')
def feedback(request):

    if request.method=='POST':
        name=request.POST['name']
        email=request.POST['email']
        content=request.POST['content']
        feedback=Feedback(name=name, email=email, content=content)
        feedback.save()
        messages.success(request,'Thank you for  your feedback')
    return render(request,'feedback.html')
#images
def photo(request):
    ph = Blog.objects.all().order_by('-id')


    context = {'ph':ph}
    return render(request,'photos.html',context)

#search images
def search_photos(request):
    query = request.GET['query']
    allposts =Blog.objects.filter(technology__icontains = query)
    params={'allposts':allposts,'query':query}
    return render(request,'imagesearch.html',params)

#allpost  images pdf vedios
def allblogs(request):
    allblogs = Blog.objects.all().order_by('-id')

    context = {'allblogs':allblogs}
    return render(request,'Allblogs.html',context)

#search allposts
def search_allblogs(request):
    t = request.GET['t']
    e =Blog.objects.filter(technology__icontains = t)
    params={'e':e,'t':t}
    return render(request,'alsearch.html',params)


#like
def like_post(request):
    user = request.user
    if request.method =='POST':
        post_id =request.POST.get('post_id')
        post_obj =Blog.objects.get(id=post_id)
        if user in post_obj.liked.all():
            post_obj.liked.remove(user)


        else:
            post_obj.liked.add(user)


        like,created =Like.objects.get_or_create(user=user,post_id=post_id)
        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'

            else:
                like.value = 'Like'
        like.save()
    return redirect(f'/d/{post_obj.id}')



#def LikeView(request,pk):
 #   post = get_object_or_404(Blog, id=request.POST.get('post_id'))
  #  post.likes.add(request.user)
   # return HttpResponseRedirect(reverse('d',args=[str(pk)]))


# detailview of post where user can comment
def d(request, id):
      allpost =Blog.objects.filter(id=id)

      comments = PostComment.objects.filter(post__in=allpost,parent=None)
      replies =  PostComment.objects.filter(post__in=allpost).exclude(parent=None)
      replydict = {}
      for reply in replies:
            if reply.parent.sno not in replydict.keys():
                replydict[reply.parent.sno]=[reply]
            else:
                replydict[reply.parent.sno].append(reply)
      context = {'allpost': allpost,'comments':comments,'user':request.user,'replydict':replydict}
      return render(request, "detail.html", context)

#comment on post
def postcomment(request):
    if request.method=='POST':
        comment=request.POST.get('comment')
        user=request.user
        postsno=request.POST.get('postsno')
        post=Blog.objects.get(id=postsno)
        parentsno=request.POST.get('parentsno')
        if parentsno == "":
            comment=PostComment(comment=comment,user=user,post=post)
            #comment.save()
            #essages.success(request,"your comment has been posted successfully")
        else:
            parent=PostComment.objects.get(sno=parentsno)
            comment=PostComment(comment=comment,user=user,post=post,parent=parent)
        comment.save()
            #messages.success(request,"your reply has been posted successfully")

    return redirect(f'/d/{post.id}')

#pdf
def pdf(request):
    p = Blog.objects.all().order_by('-id')
    context = {'p':p}
    return render(request,'postpdf.html',context)

#search pdf
def search_pdf(request):
    y = request.GET['y']
    allpdf =Blog.objects.filter(technology__icontains = y)
    context ={'allpdf':allpdf,'y':y}
    return render(request,'pdfsearch.html',context)






# post vedio
def video(request):
    u = Blog.objects.all().order_by('-id')

    context = {'u':u}
    return render(request,'video.html',context)

#search vedios
def search_video(request):
    b = request.GET['b']
    po =Blog.objects.filter(technology__icontains = b)
    context ={'po':po,'b':b}
    return render(request,'videoosearch.html',context)



#assignments
def assignment(request):
    allposts = Assignment.objects.all()

    context = {'allposts':allposts}
    return render(request,'assignments.html',context)
#search assignments
def search_assignment(request):
    z = request.GET['z']
    n = Assignment.objects.filter(technology__icontains = z)
    context ={'n':n,'z':z}
    return render(request,'assignmentsearch.html',context)


#viewassignment assignments
def view_assignment(request):
    pdf = UploadAssignment.objects.all()
    return render(request,'viewassignment.html',{'pdf':pdf})

#upload assignment
def upload_assignment(request):
   if request.method == 'POST':

       h_form = UploadAssign(request.POST, request.FILES)
       if  h_form.is_valid():

            h_form.save()
            return redirect('/viewassignment')
   else:

        h_form = UploadAssign(request.POST)
   return render(request,'uploadassignment.html',{'h_form':h_form})

#change password

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user,request.POST)
        if form.is_valid():
            v = form.save()
            update_session_auth_hash(request, v)
            return render(request,'msg after changepass.html')
    else:
        form =PasswordChangeForm(request.user)
    params= {
        'form':form,
    }
    return render(request,'changepass.html',params)


