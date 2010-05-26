from django.shortcuts import get_list_or_404, render_to_response, get_object_or_404, redirect
from django.template import RequestContext
from django.http import Http404
from django.http import HttpResponseRedirect

from django.contrib.admin.views.decorators import staff_member_required
from recipes.models import Recipe
from tagging.models import Tag, TaggedItem
from recipes.forms import RecipeForm
from django.template.defaultfilters import slugify
from django.core.urlresolvers import reverse

from django.conf import settings
from recaptcha.client import captcha
import datetime

def recipe_index(request, filter=None):
    if request.method == 'POST' and request.user.is_staff:
        recipe=Recipe.objects.get(id=request.POST.get("id", None))
        if request.POST.get("delete", None):
            return redirect('recipes-confirm-delete', slug=recipe.slug)
        else:
            if recipe.approved:
                recipe.approved=False
            else:
                recipe.approved=True
            recipe.save()
        return redirect('recipes-index')
        
    if request.user.is_staff:
        if filter == "approved":
            recipes=Recipe.approved_objects.all()
        elif filter == "unapproved":
            recipes=Recipe.objects.filter(approved=False)
        else:
            recipes=Recipe.objects.all()


    else:
        recipes=Recipe.approved_objects.all()
    return render_to_response('recipes/recipe_index.html', locals(),
                              context_instance=RequestContext(request))

@staff_member_required
def recipe_confirm_delete(request, slug):
    recipe=Recipe.objects.get(slug=slug)
    if request.method=='POST':
        try:
            recipe.delete()
            message="Recipe deleted sucessfully."
            return redirect('recipes-index')
        except:
            message="Recpie could not be deleted, please contact your adminsitrator."
            return redirect('recipes-index')
    return render_to_response('recipes/recipe_confirm_delete.html', locals(),
                              context_instance=RequestContext(request))

@staff_member_required
def recipe_approve(request):
    if request.method == 'POST':
        recipe=Recipe.objects.get(id=3)
        recipe.approved=request.POST["approved"]
        recipe.save()
        return HttpResponseRedirect(reverse('recipes-index', args=[request.GET.get("view")]))
    return HttpResponseRedirect(reverse('recipes-index', args=[request.GET.get("view")]))

def recipe_detail(request, slug):
    if request.user.is_authenticated():
	try:
       	    recipe=Recipe.objects.get(slug=slug)
        except:
 	    raise Http404
    else:
        try:
            recipe=Recipe.approved_objects.get(slug=slug)
        except:
            raise Http404

    return render_to_response('recipes/recipe_detail.html', locals(),
                              context_instance=RequestContext(request))

def recipe_create(request):
    form=RecipeForm(request.POST or None)
    # Initialize to an empty string, not None, so the reCAPTCHA call query string
    # will be correct if there wasn't a captcha error on POST.
    captcha_error = ""

    captcha_response = \
    captcha.submit(request.POST.get("recaptcha_challenge_field", None),
    request.POST.get("recaptcha_response_field", None),
    settings.RECAPTCHA_PRIVATE_KEY,
    request.META.get("REMOTE_ADDR", None))

    if not captcha_response.is_valid:
        captcha_error = "&error=%s" % captcha_response.error_code
    elif form.is_valid():
        recipe=form.save(commit=False)
        recipe.approved=False
        recipe.slug=slugify(recipe.title)
        recipe.save()
        return redirect('recipes-submitted')
        
    return render_to_response('recipes/recipe_create.html', locals(),
                              context_instance=RequestContext(request))

def recipe_submitted(request):    
    return render_to_response('recipes/recipe_submitted.html', locals(),
                              context_instance=RequestContext(request))

def recipe_tag_index(request):
    tags=Tag.objects.usage_for_model(Recipe) 
    return render_to_response('recipes/recipe_tag_index.html', locals(),
                              context_instance=RequestContext(request))

def recipe_tag_detail(request, tag):
    ''' Show all recipes tagged with <tag> '''

    recipes = TaggedItem.objects.get_by_model(Recipe, tag)
    return render_to_response('recipes/recipe_tag_detail.html', locals(),
                              context_instance=RequestContext(request))
    
