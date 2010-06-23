from django.conf import settings
from django.conf.urls.defaults import *
from recipes import views
from recipes.models import Recipe
from tagging.views import tagged_object_list

def approved_recipes(request, tag):
    queryset = Recipe.approved_objects.all()
    return tagged_object_list(request, queryset, tag, paginate_by=10,
        allow_empty=True, template_object_name='recipes')

# custom views vendors
urlpatterns = patterns('recipes.views',
    url(r'^$', view=views.recipe_index, name="recipes-index"),
    url(r'^add/$', view=views.recipe_create, name="recipes-create"),
    url(r'^submitted/$', view=views.recipe_submitted, name="recipes-submitted"),
    url(r'^approve/$', view=views.recipe_approve, name="recipes-approve"),
    url(r'^(?P<slug>[-\w]+)/$', view=views.recipe_detail, name="recipes-detail"),
    url(r'^(?P<slug>[-\w]+)/delete/$', view=views.recipe_confirm_delete, name="recipes-confirm-delete"),
    url(r'^(?P<filter>[-\w]+)/$', view=views.recipe_index, name="recipes-index"),
    #url(r'^products/$', view=views.vendor_tags, name="vendor_tag_list"),
    #url(r'^product/(?P<tag>[-_A-Za-z0-9]+)/$', view=views.vendors_with_tag, name="vendors_with_tag"), 
    #url(r'^product/(?P<tag>[-_A-Za-z0-9]+)/page/(?P<page>d+)/$', view=views.vendors_with_tag, name="vendors_with_tags_pages" ),
    url(r'^tags/$', view=views.recipe_tag_index, name="recipes-tag-index"),
    url(r'^tags/(?P<tag>[^/]+)/$', approved_recipes, name='recipes-tag-detail'),

    
)
