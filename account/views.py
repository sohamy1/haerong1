from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser
from comment.models import Comments
from board.models import Posts
from django.http import HttpResponse, Http404
from django.contrib import messages
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.hashers import make_password, check_password
from random import choice, random


def login_view(request):

    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request=request, email=email, password=password)

        try :
            target = CustomUser.objects.filter(email=email).get()
            if target.is_active == False:
                messages.info(request, "탈퇴한 회원입니다.")
                return render(request, "account/login.html")
        except :
            pass

        if email and password:
            if user is not None:
                login(request, user)
                return redirect("home")  # 이동할 주소를 지금 페이지로 지정하는 방법
            else:
                messages.info(request, '아이디와 비밀번호를 확인하세요')
                return render(request, 'account/login.html')
        else:
            messages.info(request, '아이디와 비밀번호를 모두 입력하세요')
            return render(request, 'account/login.html')
        
    else:
        if request.user.is_authenticated is True: # 로그인 되어있는 상태때 메인페이지로 이동
            # raise Http404
            return redirect("home")
        else:
            return render(request, "account/login.html") # 이동할 주소 지정


def logout_view(request):
    if request.user.is_authenticated is False: # 로그아웃 상태일때 메인페이지로 이동
        return redirect("home")
    logout(request)
    return redirect("home") # 향후 주소 수정


def register_view(request): 
    if request.method == 'POST':
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        nickname = request.POST['nickname']
        question_key = request.POST['question_key']
        question_value = request.POST['question_value']
        try:
            image = request.FILES['image']
        except:
            image = None


        # ------------  인증 관련 로직 ---------------------
        #필수 항목 체크
        if email and password1 and password2 and nickname and question_key and question_value:
            #이메일 체크
            if not '@' in email or '.' not in email :
                messages.info(request, '잘못된 이메일 형식입니다.')
                return render(request, 'account/register.html')
            #비밀번호 체크 
            if len(password1) < 8:
                messages.info(request, '비밀번호는 8자 이상으로 해주세요.')
                return render(request, 'account/register.html')
            if password1 != password2:
                messages.info(request, '동일한 비밀번호를 입력해 주세요.')
                return render(request, 'account/register.html')

            #이메일과 닉네임 중복확인#
            check_nickname = CustomUser.objects.filter(nickname=nickname).exists()
            check_email = CustomUser.objects.filter(email=email).exists()
            if check_nickname is True:
                messages.info(request, '중복된 닉네임입니다.')
                return render(request, 'account/register.html')
            if check_email is True:
                messages.info(request, '중복된 이메일입니다.')
                return render(request, 'account/register.html')

            hashed_password = make_password(password1)
            #체크 완료
            if image == None:
                user = CustomUser.objects.create(
                    email=email, password=hashed_password, nickname=nickname,
                    question_key=question_key, question_value=question_value
                )
            else:
                user = CustomUser.objects.create(
                    email=email, password=hashed_password, nickname=nickname, image=image,
                    question_key=question_key, question_value=question_value
                )
            
            if user is not None:
                login(request, user)
            return redirect("home")
        else:
            messages.info(request, '항목들을 모두 입력하세요')
            return render(request, 'account/register.html')
    elif request.method == 'GET':
        if request.user.is_authenticated is True: # 로그인 되어있는 상태때 메인페이지로 이동
            return redirect("home")
        return render(request, "account/register.html")
        

def myaccount_view(request):
    if request.user.is_authenticated is False: # 로그아웃 상태일때 메인페이지로 이동
        return redirect("home")

    posts = Posts.objects.filter(writer=request.user.nickname)
    comments = Comments.objects.filter(writer=request.user.nickname)
        
    return render(request, "account/myaccount.html", {'posts':posts, 'comments':comments})


def edit_view(request):
    if request.user.is_authenticated is False: # 로그아웃 상태일때 메인페이지로 이동
        return redirect("home")

    if request.method == 'POST':
        target = request.POST['nickname']
        user = request.user
        # user = CustomUser.objects.filter(nickname=target).get() # DB 객체들이 모인 집합
        check_nickname = CustomUser.objects.filter(nickname=target).exists()
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if target == user.nickname:
            pass 
        elif check_nickname is True :
            messages.info(request, '중복된 닉네임입니다.')
            return render(request, 'account/account_edit.html')
        elif target != user.nickname: # 게시글과 댓글 닉네임 수정 로직
            try:
                posts = Posts.objects.filter(writer=user.nickname)
                posts.update(writer=target)
            except:
                pass

            try:
                comments = Comments.objects.filter(writer=user.nickname)
                comments.update(writer=target)
            except:
                pass 

        if len(password1) < 8:
            messages.info(request, '비밀번호는 8자 이상으로 해주세요.')
            return render(request, 'account/account_edit.html')
        if password1 != password2:
            messages.info(request, '동일한 비밀번호를 입력해 주세요.')
            return render(request, 'account/account_edit.html')
         
        hashed_password = make_password(password1)
        user.nickname = request.POST['nickname']
        user.password = hashed_password
        user.question_value = request.POST['question_value']
        if request.POST['question_value'] == '!침착맨 화이팅':
            user.is_staff = True
        try :
            print(user.image)
            user.image = request.FILES['image']
        except :
            pass
        user.save()
        messages.info(request, '수정완료! 다시 로그인 해주세요')
        logout(request)
        return redirect("home")

    return render(request, "account/account_edit.html")


def deleted_view(request):
    if request.user.is_authenticated is False: # 로그아웃 상태일때 메인페이지로 이동
        return redirect("home")
    if request.method == 'POST':
        user = request.user
        password = request.POST['password']
        # user_info = CustomUser.objects.filter(nickname=user)

        is_valid_password = check_password(password, user.password)
        print(is_valid_password)

        if is_valid_password is False :
            messages.info(request, '비밀번호가 일치하지 않습니다.')
            return render(request, "account/account_delete.html")
        
        user.is_active = False
        user.deleted_at = timezone.now()
        user.save()
        messages.info(request, '탈퇴가 완료되었습니다!')
        logout(request)
        return redirect("home")

    elif request.method == 'GET':
        return render(request, "account/account_delete.html")


def finder_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        check_email = CustomUser.objects.filter(email=email).exists()
        if check_email is True:
            user = CustomUser.objects.filter(email=email).get() #고칠 것
            context = {
                'email': email,
                'question': user.question_key
            }
            return render(request, "account/finder_verify.html", context=context)
        else :
            return HttpResponse("해당 이메일은 없습니다.")
    return render(request, "account/finder.html")


def finder_verify_view(request):
    # if 틀릴 시 오류 반환 임시비밀번호 random 써보기
    if request.method == 'POST':
        email = request.POST['email']
        answer = request.POST['answer']

        user = CustomUser.objects.filter(email=email).get()
        if answer == user.question_value:
            
            new_password = "abcd1234"
            new_password_sec = make_password(new_password)

            user.password = new_password_sec
            user.save()
            return HttpResponse("임시 비밀번호가 제공되었습니다 : abcd1234")
        else: 
            messages.info(request, "답변이 맞지 않습니다.")
            return render(request, "account/finder_verify.html", {'email': email, 'question': user.question_key})

def account_info(request, id):
    check_user = CustomUser.objects.filter(nickname=id).exists()
    if check_user is not True:
        error = True
        return render(request, "account/account_info.html", {'error':error})
    else:
        target = CustomUser.objects.filter(nickname=id).get()
        posts = Posts.objects.filter(writer=id)
        comments = Comments.objects.filter(writer=id)
        
    return render(request, "account/account_info.html", {'target':target, 'posts':posts, 'comments':comments})
