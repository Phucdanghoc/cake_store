from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.models import User

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100)
    description = models.TextField()
    image_url = models.URLField(max_length=200)
    availability = models.BooleanField(default=True)
    flavor = models.CharField(max_length=50)
    size = models.CharField(max_length=50)

    class Meta:
        permissions = [
            ("can_add_product", "Can add product"),
            ("can_edit_product", "Can edit product"),
            ("can_delete_product", "Can delete product"),
            ("can_view_products", "Can view products"),
        ]

    def __str__(self):
        return f"{self.name} - {self.category} ({self.size})"


class Order(models.Model):
    status = models.CharField(max_length=20, choices=[
        ('pending', 'Chờ xử lý'),
        ('completed', 'Hoàn thành'),
        ('canceled', 'Đã hủy'),
    ], default='pending')
    saler = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    order_date = models.DateTimeField(null=True, blank=True)
    delivery_date = models.DateTimeField(null=True, blank=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    class Meta:
        permissions = [
            ("can_view_orders", "Can view orders"),
            ("can_create_order", "Can create order"),
        ]

    def __str__(self):
        return f"Order {self.id} - {self.saler} - {self.status}"

    def calculate_total_price(self):
        self.total_price = sum(item.total_price for item in self.items.all())
        self.save()

    def save(self, *args, **kwargs):
        if not self.order_date:
            self.order_date = timezone.localtime(timezone.now())
        super(Order, self).save(*args, **kwargs)

    def get_order_date_vn_time(self):
        return timezone.localtime(self.order_date)

    def get_delivery_date_vn_time(self):
        if self.delivery_date:
            return timezone.localtime(self.delivery_date)
        return None

    def get_total_quantity(self):
        return sum(item.quantity for item in self.items.all())

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    def save(self, *args, **kwargs):
        self.total_price = self.price * self.quantity
        super().save(*args, **kwargs)
        self.order.calculate_total_price()

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

class Promotion(models.Model):
    name = models.CharField(max_length=100)
    discount_type = models.CharField(max_length=20, choices=[
        ('percentage', 'Giảm theo phần trăm'),
        ('fixed_amount', 'Giảm theo số tiền cố định'),
    ])
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    products = models.ManyToManyField(Product, related_name='promotions')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Khuyến mãi"
        verbose_name_plural = "Khuyến mãi"
