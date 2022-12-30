from django.shortcuts import render
from .models import User
# Create your views here.
def index_unlog(request):
    return render(request, 'index_unlog.html')

def login(request):
    return render(request, 'login.html')

def login(request):
    if request.method == 'POST':
        user_name = request.POST.get('username','')
        pass_word = request.POST.get('password','')
        user = User.objects.filter(username=user_name)  #查看数据库里是否有该用户名
        if user:#如果存在
            user = User.objects.get(username = user_name)#读取该用户信息
            if pass_word==user.password:#检查密码是否匹配
                request.session['IS_LOGIN'] = True
                request.session['nickname'] = user.nickname
                request.session['username'] = user_name
                return render(request,'index.html',{'user':user})
            else:
                return render(request,'login.html',{'error': 'Wrong password !'})
        else:
            return render(request, 'login.html', {'error': 'User name does not exist !'})
    else:
        return render(request, 'login.html')

def logsuccess(request):
    return render(request,'index.html')

def register(request):
    if request.method =='POST':
        user_name = request.POST.get('username','')
        pass_word_1 = request.POST.get('password_1','')
        pass_word_2 = request.POST.get('password_2','')
        nick_name = request.POST.get('nickname','')
        email = request.POST.get('email','')
        avatar = request.FILES.get('avatar')
        if User.objects.filter(username = user_name):
            return render(request,'register.html',{'error':'User name has exist !'})
            #将表单写入数据库
        if(pass_word_1 != pass_word_2):
            return render(request, 'register.html', {'error': 'Please enter the same password !'})
        user = User()
        if avatar:
            user.avatar = 'media/' + user_name + '.png'
            img = Image.open(avatar)
            size = img.size
            print(size)
            # 因为是要圆形，所以需要正方形的图片
            r2 = min(size[0], size[1])
            if size[0] != size[1]:
                img = img.resize((r2, r2), Image.ANTIALIAS)
            # 最后生成圆的半径
            r3 = int(r2/2)
            img_circle = Image.new('RGBA', (r3 * 2, r3 * 2), (255, 255, 255, 0))
            pima = img.load()  # 像素的访问对象
            pimb = img_circle.load()
            r = float(r2 / 2)  # 圆心横坐标
            for i in range(r2):
                for j in range(r2):
                    lx = abs(i - r)  # 到圆心距离的横坐标
                    ly = abs(j - r)  # 到圆心距离的纵坐标
                    l = (pow(lx, 2) + pow(ly, 2)) ** 0.5  # 三角函数 半径

                    if l < r3:
                        pimb[i - (r - r3), j - (r - r3)] = pima[i, j]
            img_circle.save('blog/static/media/'+user_name+'.png')
        user.username = user_name
        user.password = pass_word_1
        user.email = email
        user.nickname = nick_name
        user.save()
            #返回注册成功页面
        return render(request,'index_unlog.html')
    else:
        return render(request,'register.html')

def forget_password(request):
    if request.method == 'POST':
        user_name = request.POST.get('username','')
        email = request.POST.get('email','')
        user = User.objects.filter(username = user_name)
        if user:
            user = User.objects.get(username = user_name)
            if(user.email == email):
                request.session['user_name'] = user_name
                return render(request,'reset.html')
            else:
                return render(request,'forget.html',{'error':'User name and e-mail does not match ！'})
        else:
            return render(request,'forget.html',{'error':'Please input the right user name '})
    else:
        return  render(request,'forget.html')

def reset(request):
    if request.method == 'POST':
        pass_word1 = request.POST.get('password1','')
        pass_word2 = request.POST.get('password2','')
        user_name = request.session['user_name']
        user = User.objects.get(username = user_name)
        if pass_word1 == pass_word2:
            user.password = pass_word1
            user.save()
            return render(request,'login.html')
        else:
            return render(request,'reset.html', {'error': 'Please enter the same password ！'})
    else:
        return render(request,'reset.html')

