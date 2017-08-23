- [x] 表单增强
- [ ] 账户
    - [x] 注册
    - [x] 登录
    - [x] 完善功能
- [x] 邮箱注册，发送确认邮箱
    - [x] 重置邮箱，重置密码
- [x] 数据库
- [x] 项目结构
- [x] 社交
    - [x] 文章、列表、详情页
    - [ ] 留言
    - [x] 评论
    - [ ] 评论分页
    - [ ] 第三方扩展
- [ ] 服务器


> 该项目有多个数据库迁移
> 使用`python manage.py db upgrade`命令创建、更新数据库
> 在`python manage.py shell`命令行模式下输入`Role.insert_roles()`更新`Role`表
> 继续输入`User.generate_fake(30)`, `Post.generate_fake(50)`创建虚拟用户、文章
> 输入`User.add_self_follows()`使虚拟用户自关注
