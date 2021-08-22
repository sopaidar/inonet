from django.shortcuts import render
from django.views.generic.base import View
from inonet.users.models import User
from works.models import Work
from django.http import JsonResponse
from django.utils.translation import gettext as _


# Create your views here.
def search_in_followings(user, q):
    result = []
    try:
        followings = user.followings['followings']
    except KeyError:
        return result
    for username in followings:
        if q in username:
            user = User.objects.get(username=username)
            avatar = "none"
            if user.avatar and user.avatar.url:
                avatar = user.avatar.url
            result.append({"username":user.username, "first_name": user.first_name, "last_name":user.last_name, "avatar": avatar, "label": _("دنبال می‌کنید")})

    return results

def search_in_users(q, search_type):
    result = []
    if search_type == "username":
        users = User.objects.filter(username__contains=q)
    for user in users:
        avatar = "none"
        if user.avatar and user.avatar.url:
            avatar = user.avatar.url
        result.append({"username":user.username, "first_name": user.first_name, "last_name":user.last_name, "avatar": avatar, "label": _("کاربر")})
        
    return result

 
class Search(View):
    def get(self, request):
        q = request.GET.get('q')
        print(q)
        result = []
        if len(q) < 3:
            return JsonResponse({"results": "none"})

        if q[0] == "@":
            q = q[1:]
            followings_result = search_in_followings(request.user, q)
            result = result + followings_result
            if len(result) > 3:               
                return JsonResponse({"result": result})
            users_result = search_in_users(q, "username")
            result = result + users_result
            return JsonResponse({"result": result})
        
        followings_result = search_in_followings(request.user, q)
        result = result + followings_result
        if len(result) > 3:               
            return JsonResponse({"result": result})
        users_result = search_in_users(q, "username")
        result = result + users_result
        return JsonResponse({"result": result})
           

