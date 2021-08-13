from django.shortcuts import render, redirect
from board.models import Posts
from comment.models import Comments
from account.models import CustomUser
from django.contrib import messages

def comment_view(request, id):
    post = Posts.objects.filter(id=id).get()

    if request.user.is_authenticated is False:
        messages.info(request, '로그인을 해주세요')
        return redirect("board:detail", post.id)
    
    comment = request.GET['comment']
    email = request.GET['user']
    post.comments_count += 1
    post.save()

    Comments.objects.create(linked_post = post.id, writer = email, body = comment)
    return redirect('board:detail', post.id)

def comment_stars_view(request, id):
    comment = Comments.objects.filter(id = id).get()
    post = Posts.objects.filter(id = comment.linked_post).get()

    if request.user.is_authenticated is False:
        messages.info(request, '로그인을 해주세요')
        return redirect("board:detail", post.id)
    
    if request.user.email in comment.liked_users:
        messages.info(request, "이미 추천을 하였습니다")
        return redirect("board:detail", post.id)

    else:
        messages.info(request, "추천되었습니다!")

        target_user = CustomUser.objects.filter(nickname = comment.writer).get()
        target_user.score += 5
        target_user.save()
        if int(target_user.score) > 5000:
            target_user.rank = "골드"
        elif int(target_user.score) > 500:
            target_user.rank = "실버"
        target_user.save()

        comment.stars += 1
        comment.liked_users = comment.liked_users + ", " + request.user.email
        comment.save()
        return redirect("board:detail", post.id)

def comment_del_view(request, id):
    comment = Comments.objects.filter(id = id).get()
    post = Posts.objects.filter(id = comment.linked_post).get()

    if request.user.is_authenticated is False:
        messages.info(request, '로그인을 해주세요')
        return redirect("board:detail", post.id)
    
    if request.user.nickname == comment.writer or request.user.is_staff == True:
        messages.info(request, '삭제되었습니다')
        comment.delete()
        post.comments_count -= 1
        post.save()
        return redirect("board:detail", post.id)
    else :
        messages.info(request, '사용자만 삭제할 수 있습니다')
        return redirect("board:detail", post.id)
    
    return render(request)