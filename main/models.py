from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from tinymce.models import HTMLField
#from django.contrib.auth.models import User


#users
#profiles
#posts ->content ,title,subject,time,number_of_comment,author,

User=get_user_model()

class Author(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic=models.ImageField()

    def __str__(self):
        return self.user.username

class Category(models.Model):
    title=models.CharField(max_length=14)
    
    def __str__(self):
        return self.title


class Post(models.Model):
    title=models.CharField(max_length=25)
    #when i make it textfiled it beome tiny
    overview=models.CharField(max_length=100)
    content=HTMLField()
    timestamp=models.DateTimeField(auto_now_add=True)
    comment_count=models.IntegerField(default=0)
    #view_count=models.IntegerField(default=0)
    author=models.ForeignKey(Author,on_delete=models.CASCADE)
    category=models.ManyToManyField(Category)
    img=models.ImageField()
    #we want to grap only three posts
    #if its true we will render them over here
    featured=models.BooleanField(null=True)

    def __str__(self):
        return self.title


    def get_absolute_url(self):
       return reverse("post",kwargs={'id':self.id})   

    
    def get_update_url(self):
       return reverse("update-post",kwargs={'id':self.id}) 

    def get_delete_url(self):
       return reverse("delete-post",kwargs={'id':self.id})   
  

    @property
    def get_comments(self):
        return self.comments.all()
    
    @property
    def view_count(self):
        return PostView.objects.filter(post=self).count()

     
    @property
    def comment_count(self):
        return Comment.objects.filter(post=self).count()

class PostView(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    post=models.ForeignKey(Post,on_delete=models.CASCADE)
    
    def __str__(self):
        return self.user.username


class Comment(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE) 
    timestamp=models.DateTimeField(auto_now_add=True)
    post=models.ForeignKey(Post,on_delete=models.CASCADE,related_name="comments")
    content=models.TextField()

    def __str__(self):
        return self.user.username
      
