from django.db import models

class Singer(models.Model):
    content = models.TextField()
    debut = models.DateField()

class Song(models.Model):
    singer = models.ForeignKey(Singer, on_delete=models.CASCADE, related_name='songs')
    release = models.DateField()
    content = models.TextField()

class Comment(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
