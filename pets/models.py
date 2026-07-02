from django.db import models

from users.models import User


# Create your models here.
class Pet(models.Model):
    PET_TYPES = [
        ('DOG', 'Dog'),
        ('CAT', 'Cat'),
        ('BIRD', 'Bird'),
        ('OTHER', 'Other'),
    ]

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    SIZE_CHOICES = [
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
    ]

    name = models.CharField(max_length=100)
    pet_type = models.CharField(max_length=10, choices=PET_TYPES)
    breed = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    size = models.CharField(max_length=1, choices=SIZE_CHOICES)
    description = models.TextField()
    story = models.TextField(blank=True,help_text="The pet's backstory and personality details")
    location = models.CharField(max_length=100)
    adoption_fee = models.DecimalField(max_digits=10, decimal_places=2)
    is_adopted = models.BooleanField(default=False)
    adopted_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True ,related_name='adopted_pets')
    image = models.ImageField(upload_to='pet_images/')
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)
    posted_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class AdoptionDemand(models.Model):
    STATUS_CHOICES = [
        ('PENDING',  'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
    ]

    user        = models.ForeignKey(User, on_delete=models.CASCADE, related_name='adoption_demands')
    pet         = models.ForeignKey('Pet', on_delete=models.CASCADE, related_name='adoption_demands')
    status      = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    requested_at= models.DateTimeField(auto_now_add=True)
    approved_by = models.ForeignKey(User, null=True, blank=True,
                                    on_delete=models.SET_NULL, related_name='approvals')
    decided_at  = models.DateTimeField(null=True, blank=True)
    experience = models.TextField(
        blank=True,
        help_text="Describe your experience with pets"
    )
    past_ownership = models.BooleanField(
        default=False,
        help_text="Have you owned pets before?"
    )
    living_arrangement = models.CharField(
        max_length=200,
        blank=True,
        help_text="Where will the pet live (apartment, house with yard, etc.)?"
    )
    motivation_letter = models.TextField(
        blank=True,
        help_text="Why do you want to adopt this pet?"
    )
    class Meta:
        unique_together = ('user','pet')   # one request per user/pet

    def __str__(self):
        return f"{self.user.username} → {self.pet.name} [{self.status}]"
