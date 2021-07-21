from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.


class Blog(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="+")
    blog_subscribers = models.ManyToManyField(User, blank=True)
    description = models.CharField(max_length=50, default=f"My blog")

    @receiver(post_save, sender=User)
    def create_user_blog(sender, instance, created, **kwargs):
        if created:
            Blog.objects.create(user=instance)

    #@receiver(post_save, sender=User)
    #def save_user_blog(sender, instance, **kwargs):
    #    instance.blog.save()

    def get_name(self):
        return self.user.get_full_name()

    @property
    def subs_count(self):
       return self.blog_subscribers.count()

    @property
    def posts_count(self):
        return Post.objects.filter(blog=self).count()


class Post(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=30)
    text = models.TextField()
    viewed = models.ManyToManyField(User, blank=True)

    def get_name(self):
        return self.blog.get_name()
