from django.db import models
from Config.Tools import RandomString
from ckeditor.fields import RichTextField
from Config.Tools import GetDifferenceTime
from Config.settings import DOMAIN_URL
import datetime


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
    def getBySlug(self,slug):
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

    def __str__(self):return self.title

    def getSlug(self):
        title = str(self.title).replace(' ','-')
        return f"{title}-{self.id}"


class CustomeManagerPost(models.Manager):

    def getPost(self,*args,**kwargs):
        return self.get_queryset().filter(published=True)

    def getPostBySearch(self,searchValue):
        return self.getPost().filter(title__icontains=searchValue)

    def getPostByCategory(self,slug):
        categoryID = str(slug).split('-')[-1]
        if categoryID.isdigit():
            return self.getPost().filter(category_id=categoryID)
        return {}

    def getPostByTag(self,slug):
        tagID = str(slug).split('-')[-1]
        if tagID.isdigit():
            return self.getPost().filter(tags__in=tagID)
        return {}

    def getPopular(self):
        return self.getPost()[:5] # Must Implemented


class Post(models.Model):
    title = models.CharField(max_length=200)
    coverImage = models.ImageField(upload_to=upload_src_cover_image,null=True,blank=True)
    video = models.FileField(upload_to=upload_src_video,null=True,blank=True)
    description = RichTextField()
    category = models.ForeignKey('Blog.Category',on_delete=models.CASCADE)
    tags = models.ManyToManyField('Blog.Tag')
    dateTimeSubmit = models.DateTimeField(auto_now_add=True)
    dateTimePublish = models.DateTimeField(auto_now=True)
    published = models.BooleanField(default=False)

    objects = CustomeManagerPost()


    def __str__(self):
        return f"{self.title[:100]}..."

    def getTimePastPublished(self):
        return GetDifferenceTime(self.dateTimePublish)

    def getSlug(self):
        title = str(self.title).replace(' ','-')
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
            return video.url
        return None

    def getCommentsCount(self):
        return 3 # Must Implemented

    def getComment(self):
        return [] # Must Implemented