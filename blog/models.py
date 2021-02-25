from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=30)
    sub_title = models.CharField(max_length=300, blank=True)
    content = models.TextField()

    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)
    file_upload = models.FileField(upload_to='blog/files/%Y/%m/%d/', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'[{self.pk}]{self.title}'

    def get_absulute_url(self):
        return f'/blog/{self.pk}'
