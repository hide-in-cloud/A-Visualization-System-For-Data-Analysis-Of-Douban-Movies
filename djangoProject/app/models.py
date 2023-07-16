from django.db import models


class MovieDetail(models.Model):
    title = models.CharField(max_length=64, blank=True, null=True)
    rate = models.DecimalField(max_digits=2, decimal_places=1, blank=True, null=True)
    detail_url = models.CharField(max_length=255, blank=True, null=True)
    cover = models.CharField(max_length=255, blank=True, null=True)
    year = models.CharField(max_length=4, blank=True, null=True)
    directors = models.CharField(max_length=255, blank=True, null=True)
    actors = models.TextField(blank=True, null=True)
    types = models.CharField(max_length=128, blank=True, null=True)
    countries = models.CharField(max_length=128, blank=True, null=True)
    lang = models.CharField(max_length=128, blank=True, null=True)
    release_date = models.CharField(max_length=128, blank=True, null=True)
    runtime = models.IntegerField(blank=True, null=True)
    rating_sum = models.IntegerField(blank=True, null=True)
    stars_proportion = models.CharField(max_length=255, blank=True, null=True)
    summary = models.TextField(blank=True, null=True)
    comment_len = models.IntegerField(blank=True, null=True)
    img_list = models.TextField(blank=True, null=True)
    video = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'movie_detail'


class MovieComment(models.Model):
    user_id = models.IntegerField(verbose_name='用户ID', blank=True, null=True)
    movie_id = models.IntegerField(verbose_name='电影ID', blank=True, null=True)
    comment_star = models.IntegerField(verbose_name='星级评分', blank=True, null=True)
    comment_content = models.TextField(verbose_name='短评内容', blank=True, null=True)
    comment_time = models.DateField(verbose_name='短评时间', blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'movie_comment'
