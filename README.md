### 由flask和Vue.js搭建的个人博客

#### 用到的框架及依赖
1. Flask框架提供Restful风格的api
2. Vue.js构建前端页面, 前端代码在[blog-frotend](https://github.com/RainJoe/blog-frontend)
3. 数据库使用MySQL

#### 博客主要功能
1. 用户登录注册
2. 博客增删改查，文章评论，图片上传
3. 后台管理，权限控制

### 如何使用
#### 安装依赖

```shell
sudo pip install -r requirements.txt
```

#### 修改``config.py``中的数据库连接地址
将``'mysql+pymysql://root:123456@localhost:3306/flaskdemo?charset=utf8'``换成你的数据库连接地址

#### 初始化数据库并添加管理员
```shell
python manage.py shell
```
进入python解释器后执行
```python

In [1]: from app import user_datastore

In [2]: role = user_datastore.create_role(name='admin')

In [3]: user = user_datastore.create_user(name='yourname', email="email@example.com", password='123456')

In [4]: user_datastore.add_role_to_user(user, role)
Out[4]: True


```

#### 让程序跑起来
```shell
python manage.py runserver
```
打开 http://localhost:5000
在 http://localhost:5000/#/login 进行登录
进入后台管理页面 http://localhost:5000/#/admin 用创建的管理员账号登录
