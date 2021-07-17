from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .decorators import user_in_group
from django.urls import resolve, reverse


@login_required
@user_in_group(group="ContentModerators")
def moderate(request):
    template_name = 'moderate/moderate.html'
    context = {
    }
    return render(request, template_name, context)
