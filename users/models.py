from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    # Tunisian states (example)
    TUNISIAN_STATES = [
        ('TN-11', 'Tunis'),
        ('TN-12', 'Ariana'),
        ('TN-13', 'Ben Arous'),
        # Add all 24 states...
    ]

    # Role choices (RBAC)
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        STAFF = 'STAFF', 'Staff'
        MEMBER = 'MEMBER', 'Member'  # Regular users

    # Gender choices
    class Gender(models.TextChoices):
        MALE = 'M', 'Male'
        FEMALE = 'F', 'Female'
        OTHER = 'O', 'Other'

    # Additional fields
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.MEMBER
    )
    profession = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=5, choices=TUNISIAN_STATES)
    city = models.CharField(max_length=100 )
    address = models.TextField()
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(
        max_length=1,
        choices=Gender.choices,
        blank=True,
        default=Gender.MALE
    )
    phone_number = models.CharField(max_length=15 , blank=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    def is_staff_member(self):
        return self.role in [self.Role.ADMIN, self.Role.STAFF]