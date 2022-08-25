from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import PROTECT, CASCADE
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):  # Customer
    tg_id = models.PositiveIntegerField(unique=True)
    name = models.CharField(max_length=200)
    code = models.PositiveIntegerField(unique=True)
    admin = models.BooleanField(default=False)
    score = models.PositiveIntegerField(default=0)
    def __str__(self) -> str:
        return f'{self.code} {self.name} {self.score}'

class Message(models.Model):
    profile = models.ForeignKey(Profile, on_delete=PROTECT)
    text = models.TextField()

    def __str__(self):
        return f'Сообщение {self.text} от {self.profile}'

class Barista(models.Model):
    User = models.OneToOneField(User, on_delete=CASCADE)
    Birthday = models.DateField(null=True, blank=True)
    Phone_number = models.PositiveBigIntegerField(blank=True, default=0)
    Addres = models.TextField(blank=True)
    
    def __str__(self):
        return self.User.__str__()

# @receiver(post_save, sender=User)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         Barista.objects.create(User=instance, Full_name=str(instance.first_name) + str(instance.last_name))

# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.barista.save()


def get_barista_today():
    return 1

class Buying(models.Model):
    def get_check(self):
        return self.id

    Check = models.IntegerField(blank=True, default=1)
    Customer = models.ForeignKey(Profile, on_delete=PROTECT, blank=True, default=1)
    Barista = models.ForeignKey(Barista, on_delete=PROTECT, blank=True, default=get_barista_today())
    Cost = models.IntegerField(blank=True, default=0)
    Paid = models.BooleanField(default=False)
    Datetime = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f'{self.id} -- {self.Check} -- {self.Customer} -- {self.Barista} -- {self.Cost} -- {self.Paid} -- {self.Datetime}'
        

class Product(models.Model):
    Name = models.CharField(max_length=200)
    Price = models.PositiveIntegerField()

    def __str__(self):
        return f'{self.Name} -- {self.Price}'

class Order(models.Model):
    Buying = models.ForeignKey(Buying, on_delete=CASCADE)
    Product = models.ForeignKey(Product, on_delete=CASCADE)
    Count = models.PositiveIntegerField(default=1)
    
    def __str__(self):
        return str(self.Buying) + str(self.Product)

class Ingredients(models.Model):
    Name = models.CharField(max_length=200)
    Count = models.IntegerField()

class Recipe(models.Model):
    Product = models.ForeignKey(Product, on_delete=PROTECT)
    Ingred = models.ForeignKey(Ingredients, on_delete=PROTECT)
    Count_ingred = models.IntegerField()

class Provider(models.Model):
    Name = models.CharField(max_length=100)
    Nomber = models.CharField(max_length=15)

class Supply(models.Model):
    Provider = models.ForeignKey(Provider, on_delete=PROTECT)
    DateRequest = models.DateField()
    DateSupply = models.DateField()
    Price = models.PositiveIntegerField()
    Delivered = models.BooleanField()

class Stock(models.Model):
    Ingred = models.ForeignKey(Ingredients, on_delete=PROTECT)
    Supply = models.ForeignKey(Supply, on_delete=PROTECT)
    Cost = models.DecimalField(max_digits=7, decimal_places=2)
    Count = models.PositiveIntegerField()