
import re

from django import template
from django.conf import settings
from django.db import models

from recipes.models import Recipe
#Recipe = models.get_model('recipes', 'recipe')

register = template.Library()

class LatestRecipes(template.Node):
    def __init__(self, limit, var_name):
        self.limit = int(limit)
        self.var_name = var_name

    def render(self, context):
        recipes = Recipe.approved_objects.all()[:self.limit]
        if recipes and (self.limit == 1):
            context[self.var_name] = recipes[0]
        else:
            context[self.var_name] = recipes
        return ''

@register.tag
def get_latest_recipes(parser, token):
    """
    Gets any number of latest recipes and stores them in a varable.

    Syntax::

        {% get_latest_recipes [limit] as [var_name] %}

    Example usage::

        {% get_latest_recipes 10 as latest_recipe_list %}
    """
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%s tag requires arguments" % token.contents.split()[0]
    m = re.search(r'(.*?) as (\w+)', arg)
    if not m:
        raise template.TemplateSyntaxError, "%s tag had invalid arguments" % tag_name
    format_string, var_name = m.groups()
    return LatestRecipes(format_string, var_name)


