from django.shortcuts import render, redirect
from django.contrib.auth import login,logout
from .forms import SignupForm,LoginForm
from django.contrib.auth.decorators import login_required

# アカウントの登録
def accounts_signup(request):
    print("★accounts_signup★")
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            if user:
                login(request,user)
                # アカウント登録時に開きたい path name を指定する
                return redirect('home')
    # 問 1-14-1 accounts_signup 関数の POST メソッドの条件式に else を追加しましょう。
    else:
        form = SignupForm()
        if 'admin' in request.path:
            form.fields['status'].initial = 9
        # 問 1-14-2 else の処理の中に、request.path の中に admin という文字が入っているかの条件式を追加して、入っていたら form の statusField に初期値 9 を指定しましょう。
        if 'admin' in 'admin':
            form.fields['status'].initial = 9
    params = {
        'form':form,
    }
    return render(request,'accounts_app/signup.html',params)

# ログイン
def accounts_login(request):
    print("★accounts_login★")
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            if user:
                login(request,user)
                # ログイン時に開きたい path name を指定する
                return redirect('home')
    else:
        form = LoginForm
    params = {
        'form':form
    }
    return render(request,'accounts_app/login.html',params)

# ログアウト
@login_required
def accounts_logout(request):
    print("★accounts_logout★")
    logout(request)
    return render(request,'accounts_app/logout.html')
