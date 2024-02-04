from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import LongToShort

# Create your views here.
def home_page(request):
    context = {
        "submitted": False,
        "error": False
    }

    if request.method == "POST":
        data = request.POST
        long_url = data['longurl']
        custom_name = data['custom_name']
        
        try:
            obj = LongToShort(long_url = long_url, short_url = custom_name)
            obj.save()

            date = obj.date
            clicks = obj.clicks

            context["long_url"] = long_url
            context["short_url"] = request.build_absolute_uri() + custom_name
            context["date"] = date
            context["clicks"] = clicks
            context["submitted"] = True
        except:
            context["error"] = True

    return render(request, "index.html", context )

def redirect_url(request, short_url):
    row = LongToShort.objects.filter(short_url = short_url)

    if len(row) == 0:
        return HttpResponse("No such short url exist")
    obj= row[0]
    long_url = obj.long_url

    obj.clicks = obj.clicks +1 
    obj.save()

    return redirect(long_url)

def all_analytics(request):

    rows = LongToShort.objects.all()

    context = {
        "rows": rows
    }

    return render(request, "all-analytics.html", context)

def analytics(request, short_url):
    rows = LongToShort.objects.get(short_url = short_url)
    context = {
       "short_url": rows.short_url,
       "long_url": rows.long_url,
       "date": rows.date,
       "clicks":rows.clicks
    }
   
    return render(request, "analytics.html", context)

def delete_url(request, short_url):
    try:
        obj = LongToShort.objects.get(short_url=short_url)
        obj.delete_url()
        HttpResponse("Short URL deleted successfully!")
        return redirect('/all-analytics')
    except:
       return HttpResponse("No such short url exist")

     