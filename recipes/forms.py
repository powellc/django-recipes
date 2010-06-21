import django.forms as forms
from recipes.models import Recipe
from markitup.widgets import MarkItUpWidget
from myutils.widgets import MakeAutoCompleteTagInput
from tagging.forms import TagField
from captcha.fields import ReCaptchaField

class RecipeForm(forms.ModelForm):
    description = forms.CharField(widget=MarkItUpWidget())
    ingredients = forms.CharField(widget=MarkItUpWidget())
    directions = forms.CharField(widget=MarkItUpWidget())
    tags = TagField(widget=MakeAutoCompleteTagInput(Recipe))
    captcha = ReCaptchaField(label="Please fill this out to verify you are are a real person.")

    class Meta:
        model=Recipe
        exclude=('approved', 'slug')
        
