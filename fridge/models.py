from django.db import models
import datetime

# Create your models here.
MEASUREMENT_UNITS = (
    (1, 'piece(s)'),
    (2, 'ml'),
    (3, 'l'),
    (4, 'mg'),
    (5, 'g'),
    (6, 'kg')
)

CATEGORIES = (
    (1, 'Fruits'),
    (2, 'Vegetables'),
    (3, 'Legumes'),
    (4, 'Grains & Cereals'),
    (5, 'Bread'),
    (6, 'Meat & Eggs'),
    (7, 'Fish & Seafood'),
    (8, 'Dairy products'),
    (9, 'Beverages'),
    (10, 'Desserts, Snacks & Sweets'),
    (11, 'Prepared food'),
    (12, 'Instant food'),
    (13, 'Spices')
)


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
    category = models.IntegerField(choices=CATEGORIES)
    quantity = models.IntegerField()
    quantityType = models.IntegerField(choices=MEASUREMENT_UNITS, default=1)
    expirationDate = models.DateField(default=datetime.date.today())
    # If open - check in category dict if long term or short term consumtion. If later max 3 days until expired
    openedDate = models.DateField(blank=True, null=True)
    # Check via method
    expiringSoon = models.BooleanField(blank=True, default=False)
    expired = models.BooleanField(blank=True, default=False)
    fridgeList = models.ForeignKey(FridgeList, on_delete=models.CASCADE, related_name='fridge')

    def quantitystr(self):
        return "{} {}".format(self.quantity, dict(MEASUREMENT_UNITS).get(self.quantityType))

    def categorystr(self):
        return "{}".format(dict(CATEGORIES).get(self.category))


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
    category = models.IntegerField(choices=CATEGORIES)
    quantity = models.IntegerField()
    quantityType = models.IntegerField(choices=MEASUREMENT_UNITS, default=1)
    # Check if in fridge list by querying Name & Category in FrdigeEntry on FridgeList on BuyList on BuyListEntry
    fridgeList = models.ForeignKey(FridgeList, on_delete=models.CASCADE)

    def quantitystr(self):
        return "{} {}".format(self.quantity, dict(MEASUREMENT_UNITS).get(self.quantityType))

    def categorystr(self):
        return "{}".format(dict(CATEGORIES).get(self.category))
