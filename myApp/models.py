from django.db import models
from django.db import models

class Cooperative(models.Model):
    co_name = models.CharField(max_length=50, unique=True)
    work = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'Cooperative'


class Admin(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50)
    phone_number = models.CharField(max_length=15)
    password = models.CharField(max_length=50)
    
    
    class Meta:
        db_table = 'Admin'

class Product(models.Model): 
    p_name = models.CharField(max_length=50)
    Description = models.CharField(max_length=500)
    co_name = models.CharField(max_length=100)
    
    class Meta:
        db_table = 'Product'

class Season(models.Model): 
    name = models.CharField(max_length=50)
    startdate = models.CharField(max_length=50)
    enddate = models.CharField(max_length=50) 
    status = models.CharField(max_length=30)
    
    class Meta:
        db_table = 'Season'

class CoUser(models.Model):  
    user_name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=15)
    role = models.CharField(max_length=50)
    co_name = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    created_at_date = models.DateTimeField(auto_now_add=True)  
    
    class Meta:
        db_table = 'co_users'

class Farmer(models.Model):
    nation = models.CharField(max_length=16, verbose_name='National ID', unique=True)
    name = models.CharField(max_length=100, verbose_name='Farmer Name')
    email = models.EmailField(verbose_name='Email')
    password = models.CharField(max_length=100, verbose_name='Password') 
    phone = models.CharField(max_length=15, verbose_name='Phone number')
    co_name = models.CharField(max_length=100, verbose_name='Co Name') 
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Registration Date')

    class Meta:
         db_table = 'Farmers'


class Inventory(models.Model):
    storekeeper_id = models.CharField(max_length=10)
    season_id = models.ForeignKey(Season, on_delete=models.CASCADE)
    co_name = models.CharField(max_length=10)
    farmer_id = models.CharField(max_length=16)
    farmer_name = models.CharField(max_length=10)
    product_name = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Registration Date')

    class Meta:
        db_table = 'Inventory'
        
class Selle(models.Model):
    co_name = models.CharField(max_length=10)
    customer_National_id = models.CharField(max_length=16)
    Customer_name = models.CharField(max_length=100)
    product_name = models.CharField(max_length=10)
    quantity = models.IntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    userid = models.CharField(max_length=20)    
    create_date = models.DateField()  # Changed to DateField for better handling
    quantity = models.CharField(max_length=10)
    unit_price = models.CharField(max_length=20) 
    userid = models.CharField(max_length=20)    
    create_date = models.CharField(max_length=30)   

    class Meta:
        db_table = 'Selles'