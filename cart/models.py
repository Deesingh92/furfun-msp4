from django.db import models
from django.contrib.auth.models import User
from shop.models import Product


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Cart #{self.pk} - User: {self.user.username}'

    def get_cart_total(self):
        return sum(item.get_item_total() for item in self.cart_items.all())

    def add_product_to_cart(self, product, quantity=1):
        cart_item, created = CartItem.objects.get_or_create(cart=self, product=product)
        cart_item.quantity += quantity
        cart_item.save()


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='cart_items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def save(self, *args, **kwargs):
        # Calculate the price based on the associated product's price
        if self.product:
            self.price = self.product.price * self.quantity
        super().save(*args, **kwargs)

    def get_item_total(self):
        if hasattr(self, 'price'):
            return self.price
        elif self.product:
            return self.product.price * self.quantity
        return 0