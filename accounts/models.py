from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    # remove the inherited username field
    username = None

    # make email the unique identifier
    email = models.EmailField(
        'email address',
        unique=True,
        blank=False,
        max_length=254,
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

    # tell Django to use email for login
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # no other required fields at create-user time

    def save(self, *args, **kwargs):
        # contractors shouldn’t have a company name
        if self.account_type == 'contractor':
            self.company_name = None
        super().save(*args, **kwargs)
