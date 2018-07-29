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
1. 安装docker
2. 修改Dockerfile中的FLASK_USER, FLASK_USER_EMAIL, FLASK_USER_PASSWORD为你的用户名，邮箱，密码
3. 修改docker-compose.yml中的MYSQL_ROOT_PASSWORD为你的数据库密码
4. 修改config.py 中ProductionConfig的数据库密码为docker-compose.yml中设置的密码
5. 在docker-compose.yml所在的文件夹下运行 ``docker-compose up --build -d``
6. 在浏览器中打开http://127.0.0.1:8080/login进行登录

