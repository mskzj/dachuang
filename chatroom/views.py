# chat/views.py
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator

from django.urls import reverse
from django.http import JsonResponse,HttpResponse

from account.models import User,Userinfo
from chatroom.models import Room,Persons
from .form import Roomform


@csrf_exempt


def chat(request):
    #判断是否登录
    username = request.session.get('username', default=None)
    context = {} #返回界面数据

    if username:
        user = User.objects.get(username=username)

        nickname = Userinfo.objects.get(user=user).nickname
        # top用户图片

        try:
            your_headimg = Userinfo.objects.get(user=user).headimg.url
        except:
            your_headimg = '/static/images/origin.jpg'  # 默认图像

        if request.method == "POST":  #创建聊天室
            room_form = Roomform(request.POST)
            if room_form.is_valid():
                room_type=room_form.cleaned_data['room_type']
                room_name=room_form.cleaned_data['room_name']
                if Room.objects.filter(room_name=room_name):
                    room_form.add_error(None, "该聊天室已经存在")
                else:
                    room = Room(user=user, room_type=room_type, room_name=room_name)
                    room.save()
                    return render(request,
                                  'chat/room.html',
                                  {
                                      'room_name': room_name,
                                      'nickname': nickname,
                                      'your_headimg': your_headimg
                                  },
                                  )
        else:#访问界面
            #聊天室信息
            room_form = Roomform()
            all_rooms = Room.objects.filter()
            #分页
            paginator = Paginator(all_rooms, 10)
            page_num = int(request.GET.get('page', 1))
            room_of_page = paginator.get_page(page_num)
            current_page = room_of_page.number
            page_range = list(range(max(current_page - 2, 1), current_page)) + list(range(current_page, min(current_page + 2, paginator.num_pages) + 1))

            context['first_shown_page_num'] = page_range[0]
            context['last_shown_page_num'] = page_range[-1]
            context['page_range'] = page_range
            context['room_of_page'] = room_of_page
            context['your_headimg'] = your_headimg
    else:
        return redirect(reverse('login'))


    context['room_form'] = room_form
    return render(request, 'chat/chat.html',context)



def room(request, room_name):
    #判断是否登录
    username = request.session.get('username', default=None)
    if username:
        user = User.objects.get(username=username)
        room = Room.objects.filter(room_name=room_name)

        nickname = Userinfo.objects.get(user=user).nickname
        try:
            your_headimg = Userinfo.objects.get(user=user).headimg.url
        except:
            your_headimg = '/static/images/origin.jpg' #默认图像

        if room:

            all_persons = Persons.objects.filter(room__in = room)
            context = {}
            context['room'] = room[0]
            context['room_name'] = room_name
            context['nickname'] = nickname
            context['your_headimg'] = your_headimg
            context['all_persons'] = all_persons

            return render(request, 'chat/room.html', context)
        else:
            return redirect(reverse('chat'))

    else:
        return redirect(reverse('login'))


# def get_person(request,room_name):
#     #判断是否登录
#     username = request.session.get('username', default=None)
#     if username:
#         if request.method == 'POST':
#             room = Room.objects.filter(room_name=room_name)
#             all_persons = Persons.objects.filter(room__in=room).values()
#             data = []
#             x = 0
#             for i in all_persons.items:
#                 data.append([])
#                 data[x].append(i.room_user.userinfo.nickname )
#                 data[x].append(i.room_user.userinfo.headimg.url )
#                 x+=1
#             return JsonResponse(data)
#         pass
#     else:
#         return redirect(reverse('login'))




