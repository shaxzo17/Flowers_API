from django.db import models
from django.contrib.auth import get_user_model
from products.models import Flower

user = get_user_model()


class Card(models.Model):
    user = models.OneToOneField(user, on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.user.first_name if self.user else "No User"

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())

class CardItem(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE, blank=True, null=True, related_name="items")
    flower = models.ForeignKey(Flower, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.flower.name

    @property
    def total_price(self):
        return self.flower.price * self.amount
