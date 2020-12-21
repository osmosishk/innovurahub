from django.contrib import admin
from .models import Setting , Slave,MemoryZone , DataHistory
# Register your models here.
admin.site.register(Setting)
admin.site.register(Slave)
admin.site.register(MemoryZone)
admin.site.register(DataHistory)