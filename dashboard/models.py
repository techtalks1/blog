from django.db import models

class Category(models.Model):
    category_name = models.CharField(max_length=255)

    def __str__(self):
        return self.category_name

class Post(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    author = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=[('Draft', 'Draft'), ('Published', 'Published')])
    is_featured = models.BooleanField(default=False)

    def __str__(self):
        return self.title
