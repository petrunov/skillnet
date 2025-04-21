from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(
        'email address',
        max_length=254,
        unique=True,
        blank=False,
        help_text='Required. Enter a valid email address.',
    )
    ACCOUNT_TYPE_CHOICES = (
        ('company', 'Company'),
        ('contractor', 'Contractor'),
    )
    account_type = models.CharField(
        max_length=20,
        choices=ACCOUNT_TYPE_CHOICES,
        help_text="Select whether this user is a company or a contractor.",
    )
    full_name = models.CharField(
        max_length=150,
        help_text="User’s legal full name."
    )
    company_name = models.CharField(
        max_length=150,
        blank=True,
        null=True,
        help_text="If a company account, the registered company name."
    )

    def save(self, *args, **kwargs):
        # ensure contractor accounts don't persist a company_name
        if self.account_type == 'contractor':
            self.company_name = None
        super().save(*args, **kwargs)
