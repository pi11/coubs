from django.db import models


class Tag(models.Model):
    title = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.title

class Coub(models.Model):
    tmp_file = models.CharField(null=True, blank=True, max_length=150)
    is_downloaded = models.BooleanField(default=False)
    is_tg_uploaded = models.BooleanField(default=False)
    is_compilation_used = models.BooleanField(default=False)
    w = models.IntegerField(default=0)
    h = models.IntegerField(default=0)
    duration = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    tags = models.ManyToManyField(Tag)
    is_good = models.BooleanField(default=True)
    
    
    def __str__(self):
        return str(self.pk)
    

class Compilation(models.Model):
    file = models.CharField(null=True, blank=True, max_length=300)
    is_tg_uploaded = models.BooleanField(default=False)
    is_yt_uploaded = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)
