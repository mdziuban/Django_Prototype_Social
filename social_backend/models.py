from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from PIL import Image


class Player(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=500)
    profilePic = models.ImageField(upload_to='uploads/', blank=True, null=True)
    suspended = models.BooleanField(default=False)
    
    def __str__(self):
        return self.user.username
    
    def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8000' + self.image.url
        return ''
    
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Player.objects.create(user=instance)
        
@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.player.save()
    
class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='post_user')
    created = models.DateTimeField(auto_now_add=True)
    text_content = models.CharField(max_length=200, blank=True)
    img_content = models.ImageField(blank=True)
    hashtags = models.CharField(max_length=200, blank=True)
    user_likes = models.ManyToManyField(User, blank=True)

    class Meta:
        ordering = ['created']
        
class Reply(models.Model):
    post_id = models.ForeignKey(Post, on_delete=models.PROTECT, related_name='post')
    user = models.ForeignKey(User, on_delete=models.PROTECT, related_name='reply_user')
    reply_created = models.DateTimeField(auto_now_add=True)
    text_content = models.CharField(max_length=200, blank=True)
    img_content = models.ImageField(blank=True)

class GameData(models.Model):
    save_file = models.JSONField()
    user_id = models.ForeignKey(Player, models.PROTECT, related_name='gamedata')

class SiteImages(models.Model):
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)

    def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8000' + self.image.url
        return ''