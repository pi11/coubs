from django.db import models


class Coub(models.Model):
    tmp_file = models.CharField(null=True, blank=True, max_length=150)
    is_downloaded = models.BooleanField(default=False)
    is_tg_uploaded = models.BooleanField(default=False)
    is_compilation_used = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.pk)
    
