from django.contrib import admin
from .models import Pet, AdoptionDemand


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'pet_type', 'breed', 'age', 'gender', 'location', 'is_adopted', 'posted_by', 'posted_date')
    list_filter = ('pet_type', 'gender', 'size', 'is_adopted', 'posted_date')
    search_fields = ('name', 'breed', 'description', 'location')
    date_hierarchy = 'posted_date'
    ordering = ('-posted_date',)


@admin.register(AdoptionDemand)
class AdoptionDemandAdmin(admin.ModelAdmin):
    list_display = ('user', 'pet', 'status', 'requested_at', 'approved_by', 'decided_at')
    list_filter = ('status', 'requested_at')
    search_fields = ('user__username', 'pet__name')
    date_hierarchy = 'requested_at'
    ordering = ('-requested_at',)