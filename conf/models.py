from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Category(models.Model):
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Author(models.Model):
    fio = models.CharField(max_length=255)

    def __str__(self):
        return self.fio


class Event(models.Model):
    title = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='category')
    description = models.TextField()
    subcategory = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True,
                                    related_name='subcategory')
    author = models.ManyToManyField(Author)
    image = models.ImageField(upload_to='event/', null=True, blank=True)


class Product(models.Model):
    title = models.CharField(max_length=255)
    price = models.PositiveIntegerField()
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=0)
    visit = models.PositiveIntegerField()


class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Task(models.Model):
    title = models.CharField(max_length=255)
    finished = models.BooleanField(default=False)
    created_date = models.DateField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


@receiver(post_save, sender=Task)
def add_s(sender, instance, created, **kwargs):
    if created:
        instance.title = instance.title + "s"
        instance.save()
        return instance
