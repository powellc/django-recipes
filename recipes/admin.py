from recipes.models import Recipe
from django.contrib import admin

class RecipeAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}
    list_display  = ['title', 'approved', 'created', 'updated']
    list_filter   = ['approved']
    ordering = ['-created']
    search_fields = ['title', 'directions', 'ingredients']
    date_hierarchy='created'
    
admin.site.register(Recipe, RecipeAdmin)
