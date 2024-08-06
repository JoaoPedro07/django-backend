from django.db import models

# Create your models here.

from django.db import models

# Create your models here.

class Toy(models.Model):
    name = models.CharField(max_length=150, blank=False, default="")
    description = models.CharField(max_length=250)
    release_date = models.DateTimeField()
    toy_category = models.CharField(max_length=200, default="Action Figure")
    was_included_in_home = models.BooleanField(default=False)
    createad = models.DateTimeField(auto_now_add=True)
    
    
    class Meta:
        ordering = ["name",]
        
    def __srt__ (self):
        return self.name