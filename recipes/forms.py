import django.forms as forms
from recipes.models import Recipe
from markitup.widgets import MarkItUpWidget
from recipes.widgets import AutoCompleteTagInput
from tagging.forms import TagField
from captcha.fields import ReCaptchaField

class RecipeForm(forms.ModelForm):
    description = forms.CharField(widget=MarkItUpWidget())
    ingredients = forms.CharField(widget=MarkItUpWidget())
    directions = forms.CharField(widget=MarkItUpWidget())
    tags = TagField(widget=AutoCompleteTagInput())
    captcha = ReCaptchaField(label="Please let us know you are a real person")

    class Meta:
        model=Recipe
        exclude=('approved', 'slug')
        
