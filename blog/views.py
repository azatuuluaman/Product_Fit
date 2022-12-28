from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import UrlForm
from Bitrix.utils import parse_data


def get_url(request):
    if request.method == 'POST':
        url = request.POST.get('url')
        parse_data(url)
        form = UrlForm(request.POST)
        if form.is_valid():
            return HttpResponseRedirect('/thanks/')
    else:
        form = UrlForm()

    return render(request, 'blog/post_list.html', {'form': form})

