# blog_instance

### Heroku 部署
[https://weqopy.herokuapp.com/](https://weqopy.herokuapp.com/)

#### Heroku 部署升级
- `heroku maintenance:on`
- `git push heroku master`
- `heroku run python manage.py deploy`
-  `heroku restart`
-  `heroku maintenance:off`

### 本地环境变量
- `export MAIL_USERNAME=<Gmail username>`
- `export MAIL_PASSWORD=<Gmail password>`  *应用专用密码*
- `export FLASKY_ADMIN=<admin email>`  *管理员邮箱*
- `export SECRET_KEY='any string'`
- `export FLASK_CONFIG='config_name'`  *生产环境应设置为`'production'`*

### 更新、使用数据库
- 使用`python manage.py db upgrade`命令创建、更新数据库
- 在`python manage.py shell`命令行模式下输入`Role.insert_roles()`更新`Role`表
- 继续输入`User.generate_fake(30)`, `Post.generate_fake(50)`创建虚拟用户、文章
- 继续输入`User.add_self_follows()`使虚拟用户自关注

### HTTPie 测试
- 需使用两个 Terminal tab，先通过`python manage.py runserver`运行服务器
- 再通过`http`命令测试 Web 服务
- 可参考[文章](http://blog.csdn.net/huang5487378/article/details/60778293)

### 总结
*2017.9.5* 整体流程第二次实现，基础框架已基本了解，部分节点需进一步掌握。

*2017.9.19* 已部署至 Heroku
