from django.db import models


class Videos(models.Model):
    title = models.CharField(max_length=200)
    videoId = models.CharField(max_length=200)
    tag = models.CharField(max_length=200)
    published = models.CharField(max_length=200)
    duration = models.CharField(max_length=200)
    thumbnail = models.CharField(max_length=200)
    url = models.CharField(max_length=200)

    def __str__(self):
        return self.videoId
