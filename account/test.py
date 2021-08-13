# def register_view(request):
#     if request.method == 'POST':
#         email = request.POST['email'] # 이메일과 닉네임 중복 확인 기능 필요
#         password1 = request.POST['password1'] # 비밀번호 확인 기능 넣기
#         password2 = request.POST['password2']
#         nickname = request.POST['nickname']
#         image = request.POST['image']
#         question_key = request.POST['question_key']
#         question_value = request.POST['question_value']

#         CustomUser.objects.create(username=email, email=email, password=password1, nickname=nickname, image=image, question_key=question_key, question_value=question_value)
#         user = authenticate(request=request, username=email, password=password1)
#         login(request, user, backend='django.contrib.auth.backends.ModelBackend')
#         return redirect('/')
#     else:
#         return render(request, "account/register.html") #가입 페이지로 이동

    # <!-- 애완동물 커뮤니티 '해롱'에 첫걸음을 내딘 것을 축하드립니다. <hr>
    # <form action="{%url 'account:register' %}" method="POST">
    #     {% csrf_token %}
    #     이메일 <input type="text" name="email">
    #     <button><a href="">중복확인</a></button> <br>
    #     비밀번호 <input type="password" name="password1"> <br>
    #     비밀번호 재확인 <input type="password" name="password2"> <br>
    #     닉네임 <input type="text" name="nickname"> 
    #     <button><a href="">중복확인</a></button> <br>
    #     프로필 사진 <input type = "file" name = "image"><hr>
    #     <strong>확인용 질문</strong> <br>
    #     아래의 질문과 답변은 나중에 아이디/비밀번호 찾기에 사용됩니다. <br> 
    #     질문 <input type="text" name="question_key"> <br>
    #     답변 <input type="text" name="question_value"> <hr>
    #     <input type="submit" value="회원가입"> 
    # </form> <hr> -->

        #----------------------_#
        # if not email or not password:
        #     messages.info(request, '아이디와 비밀번호를 모두 입력하세요')
        #     return render(request, 'account/login.html')
        # if not user:
        #     messages.info(request, '아이디와 비밀번호를 확인하세요')
        #     return render(request, 'account/login.html')
        # if user.is_active is False:
        #     messages.info(request, '탈퇴된 계정입니다.')
        #     return render(request, 'account/login.html')

        # login(request, user)

        # return redirect("/")  # 이동할 주소를 지금 페이지로 지정하는 방법
        #-----------------------#