from django.contrib import admin
from .models import Creature, Feeding, Toy, Photo

# Register your models here.
admin.site.register(Creature)
admin.site.register(Feeding)
admin.site.register(Toy)
admin.site.register(Photo)