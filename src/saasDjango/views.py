import pathlib
from django.shortcuts import render
from django.http import HttpResponse 
from visits.models import PageVisit
this_dir = pathlib.Path(__file__).resolve().parent

def home_page_view(request, *args, **kwargs):

    qs = PageVisit.objects.all()
    queryset = PageVisit.objects.filter(path=request.path)
    my_title = "My page"
    my_context = {
        "page_title": my_title,
        "page_visit_count":queryset.count(),
        "percent":queryset.count()*100.0/qs.count(),
        "total_visit_count":qs.count(),
    }
    path = request.path
    print("path", path)
    html_template="home.html"
    
    PageVisit.objects.create(path=request.path)
    return render(request, html_template,my_context)
#------------------------------------------------

def old_home_page_view(request, *args, **kwargs):
    print(this_dir)
    html_=""
    html_file_path = this_dir / "home.html"
    html_= html_file_path.read_text()
    return HttpResponse(html_)