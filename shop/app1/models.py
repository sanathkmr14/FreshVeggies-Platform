from django.db import models
from djongo import models as djongo_models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

STATE_CHOICES=(
 ('Andhra Pradesh',   'Andhra Pradesh'),
 ('Andaman and Nicobar Islands',   'Andaman and Nicobar Islands'),
 ('Arunachal Pradesh',    'Arunachal Pradesh'),
 ('Assam',   'Assam'),
 ('Bihar',   'Bihar'),
 ('Chandigarh',    'Chandigarh'),
 ('Chhattisgarh',  'Chhattisgarh'),
 ('Dadra and Nagar Haveli', 'Dadra and Nagar Haveli'),
 ('Daman and Diu',  'Daman and Diu'),
 ('Delhi',    'Delhi'),
 ('Goa',      'Goa'),
 ('Gujarat',  'Gujarat'),
 ('Haryana',  'Haryana'),
 ('Himachal Pradesh',   'Himachal Pradesh'),
 ('Jammu and Kashmir',  'Jammu and Kashmir'),
 ('Jharkhand', 'Jharkhand'),
 ('Karnataka', 'Karnataka'), 
 ('Kerala',    'Kerala'),
 ('Ladakh',    'Ladakh'),
 ('Lakshadweep',    'Lakshadweep'),
 ('Madhya Pradesh', 'Madhya Pradesh'),
 ('Maharashtra',    'Maharashtra'),
 ('Manipur',    'Manipur'),
 ('Meghalaya',  'Meghalaya'),
 ('Mizoram',    'Mizoram'),
 ('Nagaland',   'Nagaland'),
 ('Odisha',     'Odisha'),
 ('Puducherry', 'Puducherry'),
 ('Punjab',     'Punjab'),
 ('Rajasthan',  'Rajasthan'),
 ('Sikkim',     'Sikkim'),
 ('Tamil Nadu', 'Tamil Nadu'),
 ('Telangana',  'Telangana'),
 ('Tripura',    'Tripura'),
 ('Uttar Pradesh',  'Uttar Pradesh'),
 ('Uttarakhand',    'Uttarakhand'),
 ('West Bengal',    'West Bengal')
)


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES, max_length=50)

    def __str__(self):
        return self.name
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    phone = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return self.user.username


class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    #brand = models.CharField(max_length=100)
    product_image = models.ImageField(upload_to='productimg')

    def __str__(self):
        return self.title
    
    
class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.user.username} - {self.product.title}"
    
    @property
    def total_cost(self):
        return self.quantity*self.product.discounted_price
    

STATUS_CHOICES=(
    ('Accepted', 'Accepted'),
    ('Packed', 'Packed'),
    ('On The Way', 'On The Way'),
    ('Delivered', 'Delivered'),
    ('Cancel', 'Cancel')
)


class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Accepted')

    @property
    def total_cost(self):
        return self.quantity*self.product.discounted_price


class CustomerContact(models.Model):
    _id = djongo_models.ObjectIdField()
    name  = models.CharField(max_length=122)
    email = models.EmailField(max_length=122)
    phone = models.CharField(max_length=122)
    desc  = models.TextField()
    date  = models.DateField()

    def __str__(self):
        return self.name
