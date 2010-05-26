import django.forms as forms
from recipes.models import Recipe
from markitup.widgets import MarkItUpWidget
from myutils.widgets import MakeAutoCompleteTagInput
from tagging.forms import TagField


class RecipeForm(forms.ModelForm):
    ingredients = forms.CharField(widget=MarkItUpWidget())
    directions = forms.CharField(widget=MarkItUpWidget())
    tags = TagField(widget=MakeAutoCompleteTagInput(Recipe))

    class Meta:
        model=Recipe
        exclude=('approved', 'slug')
        
