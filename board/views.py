from django.shortcuts import render, redirect
from .models import Posts 
from comment.models import Comments 
from account.models import CustomUser 
from django.core.paginator import Paginator  
from django.contrib import messages
from django.db.models import Q
from django.http import HttpResponse, Http404


def detail_view(request, id):

    check = Posts.objects.filter(id=id).exists()
    if check is False:
        messages.info(request, '해당 페이지를 찾을 수 없습니다.')
        return redirect("/")

    post = Posts.objects.filter(id = id).get()
    comments = Comments.objects.filter(linked_post = post.id)
    try:
        writer_image = CustomUser.objects.filter(nickname = post.writer).get().image
    except:
        writer_image = None
    
    post.views += 1
    post.save()
    return render(request, "board/detail.html", {'post':post, 'comments':comments, 'writer_image':writer_image})

def detail_next(request, id):

    target = int(id) + 1
    check = Posts.objects.filter(id=target).exists()
    if check is False:
        for i in range(1, 10):
            target += i
            check = Posts.objects.filter(id=target).exists()
            if check is not False:
                break
        if check is False:
            messages.info(request, '해당 페이지를 찾을 수 없습니다.')
            target = int(id)   
    
    post = Posts.objects.filter(id = target).get()
    comments = Comments.objects.filter(linked_post = post.id)
    try:
        writer_image = CustomUser.objects.filter(nickname = post.writer).get().image
    except:
        writer_image = None
    
    post.views += 1
    post.save()
    return render(request, "board/detail.html", {'post':post, 'comments':comments, 'writer_image':writer_image})

def detail_back(request, id):

    target = int(id) - 1
    check = Posts.objects.filter(id=target).exists()
    if check is False:
        for i in range(1, 10):
            target -= i
            check = Posts.objects.filter(id=target).exists()
            if check is not False:
                break
        if check is False:
            messages.info(request, '해당 페이지를 찾을 수 없습니다.')
            target = int(id)

    post = Posts.objects.filter(id = target).get()
    comments = Comments.objects.filter(linked_post = post.id)
    try:
        writer_image = CustomUser.objects.filter(nickname = post.writer).get().image
    except:
        writer_image = None
    
    post.views += 1
    post.save()
    return render(request, "board/detail.html", {'post':post, 'comments':comments, 'writer_image':writer_image})


def write_view(request):
    
    if request.user.is_authenticated is False:
        messages.info(request, '로그인을 해주세요')
        return render(request, "home.html")

    if request.method == 'POST':
        title = request.POST['title']
        body = request.POST['body']
        writer = request.POST['writer']
        category = request.POST['category']
        try:
            image = request.FILES['image']
        except:
            image = None

        if image == None:
            Posts.objects.create(
                title = title, body = body, writer = writer, category = category
            ) #이미지 넣을 수 있는 로직 넣기
        else:
            Posts.objects.create(
                title = title, body = body, writer = writer, category = category, image = image
            )

        target_user = CustomUser.objects.filter(nickname = writer).get()
        target_user.score += 1
        target_user.save()
        if int(target_user.score) > 5000:
            target_user.rank = "골드"
        elif int(target_user.score) > 500:
            target_user.rank = "실버"
        target_user.save()

        newest = Posts.objects.last()
        return redirect("board:detail", newest.id)

    return render(request, "board/write.html")


def edit_view(request, id):
    post = Posts.objects.filter(id=id).get()
    
    if request.method == 'POST':
        title = request.POST['title']
        body = request.POST['body']
        category = request.POST['category']
        try:
            image = request.FILES['image']
            post.image = image
        except:
            image = None

        post.title = title
        post.body = body
        post.category = category
        post.save()
        return redirect("board:detail", post.id)

    if request.user.is_authenticated is False:
        messages.info(request, '로그인을 해주세요')
        return redirect("board:detail", post.id)

    if request.user.nickname != post.writer:
        messages.info(request, '사용자만 수정할 수 있습니다')
        return redirect("board:detail", post.id)

    return render(request, 'board/edit.html', {'post':post})


def delete_view(request, id):
    post = Posts.objects.filter(id = id).get()

    if request.user.is_authenticated is False:
        messages.info(request, '로그인을 해주세요')
        return redirect("board:detail", post.id)
    
    if request.user.nickname == post.writer or request.user.is_staff == True:
        messages.info(request, '삭제되었습니다')
        post.delete()
        return redirect("home")
    else :
        messages.info(request, '사용자만 삭제할 수 있습니다')
        return redirect("board:detail", post.id)
    
    return render(request)


def stars_view(request, id):
    post = Posts.objects.filter(id = id).get()

    if request.user.is_authenticated is False:
        messages.info(request, '로그인을 해주세요')
        return redirect("board:detail", post.id)
    
    if request.user.email in post.liked_users:
        messages.info(request, "이미 추천을 하였습니다")
        return redirect("board:detail", post.id)

    else:
        messages.info(request, "추천되었습니다!")
        target_user = CustomUser.objects.filter(nickname = post.writer).get()
        target_user.score += 10
        target_user.save()
        if int(target_user.score) > 5000:
            target_user.rank = "골드"
        elif int(target_user.score) > 500:
            target_user.rank = "실버"
        target_user.save()
        post.stars += 1
        post.liked_users = post.liked_users + ", " + request.user.email
        post.save()
        return redirect("board:detail", post.id)

# 게시판으로 이동하는 뷰 

def board_all(request):
    posts = Posts.objects.all().order_by('-created_at')

    filter_new =  request.GET.get('filter_new')
    filter_past =  request.GET.get('filter_past')
    filter_stars =  request.GET.get('filter_stars')

    if filter_new == 'true':
        posts = Posts.objects.order_by('-created_at')
    if filter_past == 'true':
        posts = Posts.objects.order_by('created_at')
    if filter_stars == 'true':
        posts = Posts.objects.order_by('-stars')
    
    paginator = Paginator(posts, 15)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    board_name = "전체"
    return render(request, "board/board.html", {'posts':posts, 'board_name':board_name})


def board_hot(request):
    posts = Posts.objects.order_by('-views')
    board_name = "인기글"
    return render(request, "board/board.html", {'posts':posts, 'board_name':board_name})


# 주제별 게시판으로 이동하는 뷰 A-Z

def board_amphibian(request):
    posts = Posts.objects.filter(category = "양서류").order_by('-created_at')
    
    filter_new =  request.GET.get('filter_new')
    filter_past =  request.GET.get('filter_past')
    filter_stars =  request.GET.get('filter_stars')

    if filter_new == 'true':
        posts = Posts.objects.order_by('-created_at').filter(category = "양서류")
    if filter_past == 'true':
        posts = Posts.objects.order_by('created_at').filter(category = "양서류")
    if filter_stars == 'true':
        posts = Posts.objects.order_by('-stars').filter(category = "양서류")

    paginator = Paginator(posts, 15)
    page = request.GET.get('page')
    posts = paginator.get_page(page)


    board_name = "양서류"
    return render(request, "board/board.html", {'posts':posts, 'board_name':board_name})


def board_bird(request):
    posts = Posts.objects.filter(category = "조류").order_by('-created_at')
    
    filter_new =  request.GET.get('filter_new')
    filter_past =  request.GET.get('filter_past')
    filter_stars =  request.GET.get('filter_stars')

    if filter_new == 'true':
        posts = Posts.objects.order_by('-created_at').filter(category = "조류")
    if filter_past == 'true':
        posts = Posts.objects.order_by('created_at').filter(category = "조류")
    if filter_stars == 'true':
        posts = Posts.objects.order_by('-stars').filter(category = "조류")
    
    paginator = Paginator(posts, 15)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    
    board_name = "조류"
    return render(request, "board/board.html", {'posts':posts, 'board_name':board_name})


def board_etc(request):
    posts = Posts.objects.filter(category = "기타").order_by('-created_at')
    
    filter_new =  request.GET.get('filter_new')
    filter_past =  request.GET.get('filter_past')
    filter_stars =  request.GET.get('filter_stars')

    if filter_new == 'true':
        posts = Posts.objects.order_by('-created_at').filter(category = "기타")
    if filter_past == 'true':
        posts = Posts.objects.order_by('created_at').filter(category = "기타")
    if filter_stars == 'true':
        posts = Posts.objects.order_by('-stars').filter(category = "기타")

    paginator = Paginator(posts, 15)
    page = request.GET.get('page')
    posts = paginator.get_page(page)


    board_name = "기타"
    return render(request, "board/board.html", {'posts':posts, 'board_name':board_name})


def board_fish(request):
    posts = Posts.objects.filter(category = "어류").order_by('-created_at')
    
    filter_new =  request.GET.get('filter_new')
    filter_past =  request.GET.get('filter_past')
    filter_stars =  request.GET.get('filter_stars')

    if filter_new == 'true':
        posts = Posts.objects.order_by('-created_at').filter(category = "어류")
    if filter_past == 'true':
        posts = Posts.objects.order_by('created_at').filter(category = "어류")
    if filter_stars == 'true':
        posts = Posts.objects.order_by('-stars').filter(category = "어류")

    paginator = Paginator(posts, 15)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    board_name = "어류"
    return render(request, "board/board.html", {'posts':posts, 'board_name':board_name})


def board_mammals(request):
    posts = Posts.objects.filter(category = "포유류").order_by('-created_at')


    filter_new =  request.GET.get('filter_new')
    filter_past =  request.GET.get('filter_past')
    filter_stars =  request.GET.get('filter_stars')

    if filter_new == 'true':
        posts = Posts.objects.order_by('-created_at').filter(category = "포유류")
    if filter_past == 'true':
        posts = Posts.objects.order_by('created_at').filter(category = "포유류")
    if filter_stars == 'true':
        posts = Posts.objects.order_by('-stars').filter(category = "포유류")

    paginator = Paginator(posts, 15)
    page = request.GET.get('page')
    posts = paginator.get_page(page)


    board_name = "포유류"
    return render(request, "board/board.html", {'posts':posts, 'board_name':board_name})


def board_reptilia(request):
    posts = Posts.objects.filter(category = "파충류").order_by('-created_at')
    
    filter_new =  request.GET.get('filter_new')
    filter_past =  request.GET.get('filter_past')
    filter_stars =  request.GET.get('filter_stars')

    if filter_new == 'true':
        posts = Posts.objects.order_by('-created_at').filter(category = "파충류")
    if filter_past == 'true':
        posts = Posts.objects.order_by('created_at').filter(category = "파충류")
    if filter_stars == 'true':
        posts = Posts.objects.order_by('-stars').filter(category = "파충류")

    paginator = Paginator(posts, 15)
    page = request.GET.get('page')
    posts = paginator.get_page(page)

    board_name = "파충류"
    return render(request, "board/board.html", {'posts':posts, 'board_name':board_name})


def search_view(request):
    search_list = Posts.objects.all().order_by('-created_at')
    
    search_key = request.GET.get('search_key') # 검색어 가져오기
    if search_key: # 만약 검색어가 존재하면
        search_list = search_list.filter(title__icontains=search_key) # 해당 검색어를 포함한 queryset 가져오기

    return render(request, 'board/search.html', {'search_list':search_list, 'input':search_key})
