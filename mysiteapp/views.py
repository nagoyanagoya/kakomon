from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetView, PasswordResetDoneView, PasswordResetCompleteView
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import dumps, loads, BadSignature, SignatureExpired
from django.template.loader import render_to_string
from django.conf import settings
from django.http import HttpResponseBadRequest
from django.urls import reverse_lazy

from .models import ProfileModel, SubjectModel, ImageModel
from operator import attrgetter
# Create your views here.

def initialfunc(request):
    return redirect('user')

def loginfunc(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('user')
        else:
            return render(request, 'login.html', {'error':'ユーザーネーム、パスワードが違います'})
    return render(request,'login.html')

def signupfunc(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        try:
            User.objects.get(email=email)
            return render(request, 'signup.html', {'error':'このメールアドレスは既に登録されています'})
        except:
            try:
                User.objects.get(username=username)
                return render(request, 'signup.html', {'error':'このユーザーネームは既に登録されています'})
            except:
                if email.endswith('mbox.nagoya-u.ac.jp') != True:
                    return render(request, 'signup.html', {'error':'全学メールアドレスを使用してください'})
                else:
                    user = User.objects.create_user(username, email, password)
                    profile = ProfileModel.objects.create_profile(User.objects.get(username=username))
                    user.is_active = False
                    user.save()
                    current_site = get_current_site(request)
                    domain = current_site.domain
                    context = {
                        'protocol': request.scheme,
                        'domain': domain,
                        'token': dumps(user.pk),
                        'user': user,
                    }
                    subject = render_to_string('mysiteapp/mail_template/create/subject.txt', context)
                    message = render_to_string('mysiteapp/mail_template/create/message.txt', context)
                    user.email_user(subject, message)
                    message1 = '仮登録が完了しました。'
                    message2 = 'メールを確認して認証を行ってください'
                    return render(request,'signup.html',{'message1':message1,'message2':message2})
    return render(request, 'signup.html')

class CompleteView(TemplateView):
    template_name = 'complete.html'
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60*60*24)
    def get(self, request, **kwargs):
        token = kwargs.get('token')
        try:
            user_pk = loads(token, max_age=self.timeout_seconds)
        except SignatureExpired:
            return HttpResponseBadRequest()
        except BadSignature:
            return HttpResponseBadRequest()
        else:
            try:
                user = User.objects.get(pk=user_pk)
            except User.DoesNotExist:
                return HttpResponseBadRequest()
            else:
                if not user.is_active:
                    user.is_active = True
                    user.save()
                    return super().get(request, **kwargs)
        return HttpResponseBadRequest()

@login_required
def userfunc(request):
    user = request.user
    subject = ProfileModel.objects.get(user=user).subject
    sub_data = SubjectModel.objects.all()
    data = {'user':user}
    for item in sub_data:
        if item.name in subject:
            data[item.day] = item.name
    return render(request,'user.html',data)

def logoutfunc(request):
     logout(request)
     return redirect('login')

@login_required
def updatefunc(request):
    user = request.user
    object = ProfileModel.objects.get(user=user)
    if request.method == 'POST':
        object.subject = 'None'
        results = request.POST.getlist('subject')
        for item in results:
            object.subject = object.subject + ' ' + item
        object.save()
        return redirect('user')
    else:
        choices = SubjectModel.objects.all()
        subject = object.subject
        data = {'subject':subject}
        for item in choices:
            data[item.day] = item.name
        return render(request,'update.html', data)

@login_required
def detailfunc(request, name):
    object = ImageModel.objects.all()
    user = request.user.username
    image = []
    year = []
    log = ''
    for item in sorted(object,key=attrgetter('year','when','page')):
        if item.subject.name == name:
            image.append(item)
            if log != item.year:
                log = item.year
                year.append(log)
    return render(request, 'detail.html', {'user':user,'name':name,'image':image,'year':sorted(year,reverse=True)})

@login_required
def uploadfunc(request,name):
    user = request.user
    subject = SubjectModel.objects.get(name=name)
    if request.method == 'POST':
        object = ImageModel.objects.create(
            subject = subject,
            image = request.FILES['image'],
            year = request.POST['year'],
            page = request.POST['page'],
            author = request.user.username,
            when = request.POST['when'],
        )
        object.save()
        return redirect('detail', name)
    return render(request,'upload.html',{'user':user, 'name':name})

@login_required
def deletefunc(request, name, pk):
    object = ImageModel.objects.get(pk=pk)
    object.delete()
    return redirect('detail', name)

class PasswordReset(PasswordResetView):
    subject_template_name = 'mysiteapp/mail_template/password_reset/subject.txt'
    email_template_name = 'mysiteapp/mail_template/password_reset/message.txt'
    template_name = 'reset.html'
    success_url = reverse_lazy('reset_done')

class PasswordResetDone(PasswordResetDoneView):
    template_name = 'reset_done.html'

class PasswordResetConfirm(PasswordResetConfirmView):
    success_url = reverse_lazy('login')
    template_name = 'reset_confirm.html'

class PasswordResetComplete(PasswordResetCompleteView):
    template_name = 'reset_complete.html'

def resendfunc(request):
    if request.method == 'POST':
        email = request.POST['email']
        try:
            user = User.objects.get(email=email)
            current_site = get_current_site(request)
            domain = current_site.domain
            context = {
                'protocol': request.scheme,
                'domain': domain,
                'token': dumps(user.pk),
                'user': user,
            }
            subject = render_to_string('mysiteapp/mail_template/create/subject.txt', context)
            message = render_to_string('mysiteapp/mail_template/create/message.txt', context)
            user.email_user(subject, message)
            message1 = 'メールを送信しました。'
            message2 = 'メールを確認して認証を行ってください'
            return render(request,'resend.html',{'message1':message1,'message2':message2})
        except:
            return render(request,'resend.html',{'error':'アドレスを確認してください'})
    return render(request,'resend.html')