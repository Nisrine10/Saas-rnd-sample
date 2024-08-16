from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest,HttpResponse
from django.contrib.auth import get_user_model

User=get_user_model()

@login_required
def profile_list_view(request):
    context={
        "object_list": User.objects.filter(is_active=True)
    }
    return render(request,"profiles/list.html",context)



@login_required
def profile_view(request,username=None, *args, **kwargs):

    user = request.user
    print('user.has_perm("auth.view_user")',user.has_perm("auth.view_user") )
    print('user.has_perm("visits.view_pagevisit")',user.has_perm("visits.view_pagevisit") )

    #<app_label>.view_<model_name>
    #<app_label>.add<model_name>
    #<app_label>.change<model_name>
    #<app_label>.delete_<model_name>


    #profile_user_obj = User.objects.get(username=username)
    profile_user_obj = get_object_or_404(username=username)

    is_me= profile_user_obj == user

    if is_me:
        if user.has_perm("visits.view_pagevisit"):
            pass
           # qs=PageVisit.objects.all()
    return HttpResponse(f"Hello there {username}!-{profile_user_obj.id} -{user.id} - {is_me}" )