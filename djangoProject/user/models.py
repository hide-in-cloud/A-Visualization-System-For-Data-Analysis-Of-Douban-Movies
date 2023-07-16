from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from datetime import datetime
import uuid
import os


def user_avatar_path(instance, filename):
    """将图片名称换成uuid，防止重名覆盖"""
    img_type = filename.split('.')[-1]
    img_name = '{}/{}.{}'.format(instance.id, str(uuid.uuid4()).replace('-', ''), img_type)
    # 上传图片的路径
    return os.path.join('avatar/', img_name)


class UserInfo(models.Model):
    username = models.CharField(verbose_name='用户名', max_length=32, unique=True)
    password = models.CharField(verbose_name='密码', max_length=64)
    # 路径存放位置: setting.py中的MEDIA_ROOT + upload_to
    # 数据库存放的数据: upload_to + imgName
    avatar = models.ImageField(verbose_name='头像', upload_to=user_avatar_path, blank=True, null=True)
    role_choices = (
        ('admin', '管理员'),
        ('user', '用户'),
    )
    role = models.CharField(verbose_name='角色', max_length=32, choices=role_choices, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'user_info'


class UserToken(models.Model):
    token = models.CharField(max_length=64)  # 只要用户登录，生成一个随机字符串，存到这,再次登录，更新
    user = models.OneToOneField(to='UserInfo', on_delete=models.CASCADE)

    class Meta:
        managed = True
        db_table = 'user_token'


class UserFavorites(models.Model):
    """ 用户收藏夹，存储电影id """
    user = models.ForeignKey(verbose_name="用户(uid)", to='UserInfo', on_delete=models.DO_NOTHING)
    favor = models.ForeignKey(verbose_name="用户收藏的电影(mid)", to='app.MovieDetail', to_field='id', on_delete=models.DO_NOTHING)
    create_time = models.DateTimeField(verbose_name='创建时间', default=datetime.now())

    class Meta:
        managed = True
        db_table = 'user_favorites'


class UserRating(models.Model):
    user = models.ForeignKey(verbose_name="用户ID", to='UserInfo', on_delete=models.DO_NOTHING)
    movie = models.ForeignKey(verbose_name="电影ID", to='app.MovieDetail', to_field='id', on_delete=models.DO_NOTHING)
    star_rating = models.IntegerField(verbose_name='星级评分', validators=[MaxValueValidator(5), MinValueValidator(1)])
    create_time = models.DateTimeField(verbose_name='创建时间', default=datetime.now())

    class Meta:
        managed = True
        db_table = 'user_rating'
