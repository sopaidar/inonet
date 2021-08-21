from django.shortcuts import render
from django.views.generic.base import View
from inonet.users.models import User
from works.models import Work
from django.http import JsonResponse

# Create your views here.

def serialize_result(raw_result):
    print(raw_result)
    result = []
    for k, v in raw_result.items():
        if v == "username":
            user = User.objects.get(username=k)
            avatar = "none"
            if user.avatar and user.avatar.url:
                avatar = user.avatar.url
            result.append({"username":user.username, "first_name": user.first_name, "last_name":user.last_name, "avatar": avatar})
    return result

class Search(View):
    def get(self, request):
        data = "none"
        q = request.GET.get('q')
        print(q)
        if len(q) < 3:
            return JsonResponse({"results": "none"})
        result = {}
        if q[0] == "@":
            q = q[1:]
            followings = request.user.followings['followings']
            print(followings)
            for username in followings:
                if q in username:
                    result[username] = "username"
            print(result)
        
            # if len(result) < 3:

        
        data = serialize_result(result)    
        return JsonResponse({"result": data})
