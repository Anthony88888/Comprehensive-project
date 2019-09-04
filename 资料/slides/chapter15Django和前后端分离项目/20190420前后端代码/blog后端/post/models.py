from django.db import models
from user.models import User
# Create your models here.


class Post(models.Model):
    class Meta:
        db_table = 'post'

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=120, null=False)
    postdate = models.DateField(null=False)

    # 作者
    author = models.ForeignKey(User) # 自动生成外键，而且字段会变成什么呢？
    # 以后可以怎么访问？postinstance.author_id  postinstance.author?
    # content 内容 self.content.content

    def __repr__(self):
        return "<Post {} {} {}--- {}>".format(
            self.id, self.pk, self.title, self.content
        )

    __str__ = __repr__

class Content(models.Model):
    class Meta:
        db_table = 'content'

    # 如果在model中，不写主键，那么就会自动增加一个名为id的自增主键
    post = models.OneToOneField(Post) # 直接访问 post_id
    content = models.TextField(null=False)

    def __repr__(self):
        return "<Content {} {} {}--- >".format(
            self.id, self.post.id, self.content[:20]
        )

    __str__ = __repr__

