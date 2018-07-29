from django.contrib import admin
from Quiz.models import Quiz, Values, Comments, DatesPlaces

# Register your models here.


admin.site.register(Quiz)
admin.site.register(Values)
admin.site.register(Comments)
admin.site.register(DatesPlaces)
