from django.db import models
from Config.Tools import RandomString
from ckeditor.fields import RichTextField
from Config.Tools import GetDifferenceTime
from Config.settings import DOMAIN_URL
from django.db.models import F, Count
from django.db.models.functions import Coalesce
import datetime
import random


def upload_src_cover_image(instance, path):
    frmt = str(path).split('.')[-1]
    dateTime = datetime.datetime.now().strftime('%Y-%m-%d')
    src = f"post/images/cover/{dateTime}/{RandomString()}.{frmt}"
    return src


def upload_src_video(instance, path):
    frmt = str(path).split('.')[-1]
    dateTime = datetime.datetime.now().strftime('%Y-%m-%d')
    src = f"post/videos/{dateTime}/{RandomString()}.{frmt}"
    return src


class CustomizeManagerCategory(models.Manager):
    def getBySlug(self, slug):
        categoryID = str(slug).split('-')[-1]
        if categoryID.isdigit():
            return self.get_queryset().filter(id=categoryID).first()
        return None


class Category(models.Model):
    title = models.CharField(max_length=50)

    objects = CustomizeManagerCategory()

    def __str__(self):
        return self.title

    def getSlug(self):
        return f"{self.title}-{self.id}"

    def getCountPosts(self):
        return self.post_set.count()


class CustomizeManagerTag(models.Manager):
    def getBySlug(self, slug):
        tagID = str(slug).split('-')[-1]
        if tagID.isdigit():
            return self.get_queryset().filter(id=tagID).first()
        return None


class Tag(models.Model):
    title = models.CharField(max_length=50)

    objects = CustomizeManagerTag()

    def __str__(self): return self.title

    def getSlug(self):
        title = str(self.title).replace(' ', '-')
        return f"{title}-{self.id}"


class CustomeManagerPost(models.Manager):

    def getPosts(self, *args, **kwargs):
        return self.get_queryset().filter(published=True)

    def getPost(self, id):
        return self.get_queryset().filter(id=id, published=True).first()


    def getNextPost(self, nowObject):  # nowObject => id object
        try:
            nowObject = int(nowObject) + 1
            return self.get_queryset().filter(id=nowObject, published=True).first()
        except:
            return None

    def getPrevPost(self, nowObject):  # nowObject => id object
        try:
            nowObject = int(nowObject) - 1
            return self.get_queryset().filter(id=nowObject, published=True).first()
        except:
            return None


    def getPostBySearch(self, searchValue):
        return self.getPosts().filter(title__icontains=searchValue)


    def getPostByCategory(self, slug):
        categoryID = str(slug).split('-')[-1]
        if categoryID.isdigit():
            return self.getPosts().filter(category_id=categoryID)
        return {}

    def getPostByTag(self, slug):
        tagID = str(slug).split('-')[-1]
        if tagID.isdigit():
            return self.getPosts().filter(tags__in=tagID)
        return {}

    def getPopular(self):
        posts = self.getPosts().annotate(countLike=Coalesce(Count(F('likePost')),0))
        posts = posts.order_by('-countLike')
        return posts[:5]


class Post(models.Model):
    title = models.CharField(max_length=200)
    coverImage = models.ImageField(upload_to=upload_src_cover_image, null=True, blank=True)
    video = models.FileField(upload_to=upload_src_video, null=True, blank=True)
    description = RichTextField()
    category = models.ForeignKey('Blog.Category', on_delete=models.CASCADE)
    tags = models.ManyToManyField('Blog.Tag')
    dateTimeSubmit = models.DateTimeField(auto_now_add=True)
    dateTimePublish = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)

    objects = CustomeManagerPost()

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return f"{self.title[:70]}..."

    def getTimePastPublished(self):
        return GetDifferenceTime(self.dateTimePublish)

    def getRelatedPosts(self):
        relatedPosts = Post.objects.getPosts().filter(category_id=self.category.id,tags__in=self.tags.all()).exclude(id=self.id)
        return relatedPosts[:6]

    def getSlug(self):
        title = str(self.title).replace(' ', '-')
        return f"{title}-{self.id}"

    def stateWithVideo(self):
        video = self.video
        if video != None and video != '':
            return True
        return False

    def getUrlCover(self):
        media = self.coverImage
        if media != None and media != '':
            media = f"{DOMAIN_URL}{media.url}"
        else:
            media = f'{DOMAIN_URL}/assets/images/default/image-default-post.jpg'
        return media

    def getUrlVideo(self):
        video = self.video
        if video != None and video != '':
            return f"{DOMAIN_URL}{video.url}"
        return None

    def getLikesCount(self):
        return self.likePost.count()

    def getCommentsCount(self):
        return self.getComments().count()

    def getComments(self):
        return self.comment_set.filter(is_checked=True).all()


def RandomSrcImage():
    return f"{DOMAIN_URL}/assets/images/default/imageProfileComment/{random.randint(1,11)}.jpg"

class Comment(models.Model):
    key = models.CharField(max_length=150)
    post = models.ForeignKey('Blog.Post',on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    message = models.TextField()
    is_checked = models.BooleanField(default=False)
    dateTimeSubmit = models.DateTimeField(auto_now=True)
    imageProfile = models.CharField(max_length=300,default=RandomSrcImage)
    replied = models.BooleanField(default=False)
    replied_comment = models.ForeignKey('Blog.Comment',on_delete=models.SET_NULL,null=True,blank=True)

    class Meta:
        ordering = ['-id']

    def __str__(self):
        return self.name

    def getTimePast(self):
        return GetDifferenceTime(self.dateTimeSubmit)


class SavePost(models.Model):
    post = models.ForeignKey('Blog.Post',on_delete=models.CASCADE)
    key = models.CharField(max_length=150)

    def __str__(self):
        return self.key


class LikePost(models.Model):
    post = models.ForeignKey('Blog.Post',on_delete=models.CASCADE,related_name='likePost')
    key = models.CharField(max_length=150)

    def __str__(self):
        return self.key
