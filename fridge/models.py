from django.conf import settings
from django.db import models
from django.utils import timezone

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
    (13, 'Spices'),
    (14, 'Condiments')
)


class FridgeList(models.Model):
    title = models.CharField(max_length=60)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class SecurityQuestions(models.Model):
    answer = models.CharField(max_length=60)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

class FridgeEntry(models.Model):
    class Meta:
        verbose_name_plural = 'Fridge Entries'

    # ID added as PK automatically upon creation in DB
    title = models.CharField(max_length=60)
    category = models.IntegerField(choices=CATEGORIES)
    quantity = models.IntegerField()
    quantityType = models.IntegerField(choices=MEASUREMENT_UNITS, default=1)
    expirationDate = models.DateField(blank=True, null=True, default=None)
    # If open - check in category dict if long term or short term consumtion. If later max 3 days until expired
    openedDate = models.DateField(blank=True, null=True)
    # Check via method
    expiringSoon = models.BooleanField(blank=True, default=False)
    expired = models.BooleanField(blank=True, default=False)
    fridgeList = models.ForeignKey(FridgeList, on_delete=models.CASCADE, related_name='fridge')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def quantitystr(self):
        return "{} {}".format(self.quantity, dict(MEASUREMENT_UNITS).get(self.quantityType))

    def categorystr(self):
        return "{}".format(dict(CATEGORIES).get(self.category))


class BuyList(models.Model):
    # ID added as PK automatically upon creation in DB
    # Better fixed naming <FridgeList.title> Buy List
    title = models.CharField(max_length=60)
    fridgeList = models.ForeignKey(FridgeList, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

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
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def quantitystr(self):
        return "{} {}".format(self.quantity, dict(MEASUREMENT_UNITS).get(self.quantityType))

    def categorystr(self):
        return "{}".format(dict(CATEGORIES).get(self.category))
