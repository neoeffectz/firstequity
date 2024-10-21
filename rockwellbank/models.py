from django.db import models
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from cloudinary.models import CloudinaryField
# Create your models here.

class Portfolio(models.Model):
    CURRENCY_CHOICES = [
        ('$', 'Dollar'),
        ('£', 'Pound'),
        ('€', 'Euro'),
        ('₩', 'Korean Won'),
    ]
    username= models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    first_name = models.CharField(max_length=500, blank= True, null = True)
    last_name = models.CharField(max_length=200, blank= True, null = True)
    account_number = models.CharField(max_length=200, blank= True, null = True)
    city = models.CharField(max_length=200, blank= True, null = True)
    Country = models.CharField(max_length=200, blank= True, null = True)
    state = models.CharField(max_length=200, blank= True, null = True)
    address = models.CharField(max_length=200, blank= True, null = True)
    phone_number = models.IntegerField( blank= True, null = True)
    zipcode = models.IntegerField( blank= True, null = True)
    profile_image = CloudinaryField('image', blank=True, null=True)
    account_total = models.IntegerField(blank= True, null = True)
    pin = models.IntegerField(null= True, blank= True)
    amount_sign = models.CharField(max_length=1, choices=CURRENCY_CHOICES, blank=True, null=True)
    

    def __str__(self):
        return self.first_name if self.first_name else ''
    
    def get_image_name(self):
        return str(self.profile_image) if self.profile_image else ''
    
    @property
    def imageURL(self):
        try:
            url = self.profile_image.url
        except:
            url = ''
        return url
    
class Transactions(models.Model):

    DEBIT = 'Debit'
    CREDIT = 'Credit'
    ACCOUNT_TYPE_CHOICES = [
        (DEBIT, 'Debit'),
        (CREDIT, 'Credit'),
    ]
    CURRENCY_CHOICES = [
        ('$', 'Dollar'),
        ('£', 'Pound'),
        ('€', 'Euro'),
        ('₩', 'Korean Won'),
    ]
    username = models.ForeignKey(Portfolio, on_delete=models.SET_NULL, blank= True, null = True)
    id = models.AutoField(primary_key=True)
    beneficiary_name = models.CharField(max_length=200, blank= True, null = True)
    account_number = models.CharField(max_length=200, blank= True, null = True)
    branch_name = models.CharField(max_length=200, blank= True, null = True)
    bank_address = models.CharField(max_length=200, blank= True, null = True)
    bank_name = models.CharField(max_length=200, blank= True, null = True)
    account_type = models.CharField(max_length=200, blank= True, null = True)
    amount_to_transfer = models.IntegerField()
    beneficiary_email = models.EmailField(max_length=200, blank= True, null = True)
    senders_phone_number = models.CharField(max_length=15, blank= True, null = True)
    bank_swift_code = models.CharField(max_length=200, blank= True, null = True)
    transfer_pin = models.IntegerField(null=True, blank=True)
    transaction_date = models.DateField(default=timezone.now)
    transaction_type = models.CharField(max_length=200, choices=ACCOUNT_TYPE_CHOICES, null=True, blank=True)
    purpose_of_the_transfer = models.CharField(max_length=200, blank= True, null = True)
    amount_sign = models.CharField(max_length=1, choices=CURRENCY_CHOICES, blank=True, null=True)
    

    def __str__(self):
        return self.beneficiary_name
    


    


    



    