from django.db import models
from django.contrib.auth.hashers import make_password
from django.utils.crypto import get_random_string

WHERE = (
    ('D', 'desenvolvimento')
    ('H', 'homologação'),
    ('P', 'produção'),
)

LEVELS = (
    ('C', 'critical'),
    ('D', 'debug'),
    ('E', 'error'),
    ('I', 'information')
    ('W', 'warning'),
)

# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=256)

    email = models.EmailField(max_length=256)
    password = models.CharField(max_length=256)

    token = models.CharField(max_length=256, default=get_random_string(256))

    def save(*args, **kwargs):
        self.password = make_password(self.password)

        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.username


class Event(models.Model):
    findWhere = models.CharField(choices=WHERE, max_length=1)
    level = models.CharField(choices=LEVELS, max_length=1)

    address = models.IPAddressField()
    date = models.DateField(auto_now=True)

    title = models.CharField(max_length=256)
    details = models.CharField(max_length=512)
    filed = models.BooleanField()

    quantity = models.IntegerField(default=0)
    findBy = models.ForeignKey("center.User", on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.title
