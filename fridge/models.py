from django.db import models


# Create your models here.
class Account(models.Model):
    # ID added as PK automatically upon creation in DB
    username = models.CharField(max_length=60)
    # tbc.
    pw = models.CharField(max_length=60)
    # Get consolidated buy list by querying buylistentry on buylist on fridgelist on user


class FridgeList(models.Model):
    # ID added as PK automatically upon creation in DB
    title = models.CharField(max_length=60)
    # user = models.ForeignKey(Account, on_delete=models.CASCADE)


class FridgeEntry(models.Model):
    class Meta:
        verbose_name_plural = 'Fridge Entries'

    # ID added as PK automatically upon creation in DB
    title = models.CharField(max_length=60)
    category = models.CharField(max_length=60)
    quantity = models.IntegerField()
    quantityType = models.CharField(max_length=60)
    expirationDate = models.DateField()
    # If open - check in category dict if long term or short term consumtion. If later max 3 days until expired
    openedDate = models.DateField(blank=True)
    # Check via method
    expiringSoon = models.BooleanField()
    expired = models.BooleanField()
    # fridgeList = models.ForeignKey(FridgeList, on_delete=models.CASCADE)


class BuyList(models.Model):
    # ID added as PK automatically upon creation in DB
    # Better fixed naming <FridgeList.title> Buy List
    title = models.CharField(max_length=60)
    fridgeList = models.ForeignKey(FridgeList, on_delete=models.CASCADE)
    # Get all entries via query


class BuyListEntry(models.Model):
    class Meta:
        verbose_name_plural = 'Buy List Entries'

    # ID added as PK automatically upon creation in DB
    title = models.CharField(max_length=60)
    category = models.CharField(max_length=60)
    quantity = models.IntegerField()
    quantityType = models.CharField(max_length=60)
    # Check if in fridge list by querying Name & Category in FrdigeEntry on FridgeList on BuyList on BuyListEntry
    buyList = models.ForeignKey(FridgeList, on_delete=models.CASCADE)
