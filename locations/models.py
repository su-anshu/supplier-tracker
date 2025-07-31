# locations/models.py
from django.db import models

class State(models.Model):
    """Indian States"""
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)
    
    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name

class District(models.Model):
    """Districts within states"""
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='districts')
    
    class Meta:
        ordering = ['state__name', 'name']
        unique_together = ['name', 'state']
    
    def __str__(self):
        return f"{self.name}, {self.state.name}"
    
    @property
    def full_name(self):
        return f"{self.name}, {self.state.name}"

class City(models.Model):
    """Major Indian Cities for Serviceable Locations"""
    name = models.CharField(max_length=100, unique=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='cities')
    is_major = models.BooleanField(default=False, help_text="Major business city")
    
    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Cities'
    
    def __str__(self):
        return f"{self.name}, {self.state.name}"
    
    @property
    def full_name(self):
        return f"{self.name}, {self.state.name}"
