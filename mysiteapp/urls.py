from django.urls import path
from .views import loginfunc, signupfunc, userfunc, logoutfunc, initialfunc,updatefunc
from .views import uploadfunc, deletefunc, resendfunc, detailfunc
from .views import CompleteView, PasswordResetConfirm, PasswordReset, PasswordResetDone

urlpatterns = [
    path('', initialfunc, name='initial'),
    path('login/', loginfunc, name='login'),
    path('signup/', signupfunc, name='signup'),
    path('user/', userfunc, name='user'),
    path('logout/', logoutfunc, name='logout'),
    path('update/', updatefunc, name='update'),
    path('detail/<str:name>/', detailfunc, name='detail'),
    path('upload/<str:name>/', uploadfunc, name='upload'),
    path('delete/<str:name>/<int:pk>', deletefunc, name='delete'),
    path('complete/<token>', CompleteView.as_view(), name='complete'),
    path('reset/', PasswordReset.as_view(), name='reset' ),
    path('reset/done/', PasswordResetDone.as_view(), name='reset_done'),
    path('reset/<uidb64>/<token>/', PasswordResetConfirm.as_view(), name='reset_confirm'),
    path('resend/', resendfunc, name='resend'),
]