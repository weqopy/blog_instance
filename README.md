# blog_instance

> 更新、使用数据库
- 使用`python manage.py db upgrade`命令创建、更新数据库
- 在`python manage.py shell`命令行模式下输入`Role.insert_roles()`更新`Role`表
- 继续输入`User.generate_fake(30)`, `Post.generate_fake(50)`创建虚拟用户、文章
- 继续输入`User.add_self_follows()`使虚拟用户自关注

> HTTPie 测试
- 需使用两个 Terminal tab，先通过`python manage.py runserver`运行服务器
- 再通过`http`命令测试 Web 服务
- 可参考[文章](http://blog.csdn.net/huang5487378/article/details/60778293)
