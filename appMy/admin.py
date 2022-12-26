from django.contrib import admin
from .models import *

# Register your models here.



class CardAdmin(admin.ModelAdmin):
    '''Admin View for Category'''
    list_display = ('title', 'priece', 'id')
    search_fields = ('title','id','priece')

    list_filter = ('date_now',) 
    date_hierarchy = 'date_now'
    # raw_id_fields = ('',)
    # readonly_fields = ('',)
    # ordering = ('date_now',)

    
class CategoryAdmin(admin.ModelAdmin):
    '''Admin View for Category'''

    list_display = ('name','id')


admin.site.register(Card, CardAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment)
admin.site.register(Userinfo)
