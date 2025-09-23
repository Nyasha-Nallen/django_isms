from django.db import models
from accounts.models import CustomUser

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.name:
            self.name = self.name.title()
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'categories'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100, unique=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name="products")
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    quantity = models.PositiveIntegerField(default=0)
    created_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.name:
            self.name = self.name.title()
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'products'
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name

class StockEntry(models.Model):
    received_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'stock-entries'

    def __str__(self):
        return f"Stock Entry #{self.id} by {self.received_by}"
    
class StockEntryItem(models.Model):
    receipt = models.ForeignKey(StockEntry, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.product.quantity += self.quantity
            self.product.save()
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'stock_enrty_items'

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

class SaleTransaction(models.Model):
    sold_by = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    sale_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        db_table = 'sale_transactions'

    def __str__(self):
        return f"Sale #{self.id} by {self.sold_by}"
    
    def update_total(self):
        """Recalculate and save the total for this sale."""
        total = sum(item.line_total for item in self.items.all())
        self.sale_total = total
        self.save()


class SaleItem(models.Model):
    sale = models.ForeignKey(SaleTransaction, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    line_total = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def save(self, *args, **kwargs):
        # Calculate line_total before saving
        self.line_total = self.product.price * self.quantity 

        # Only subtract stock on creation (not update)
        if self.pk is None:
            if self.product.quantity >= self.quantity:
                self.product.quantity -= self.quantity
                self.product.save()
            else:
                raise ValueError(f"Not enough stock for {self.product.name}")
        super().save(*args, **kwargs)

    class Meta:
        db_table = 'sale_items'


    def __str__(self):
        return f"{self.quantity} x {self.product.name}"