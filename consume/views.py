from django.shortcuts import render
import requests
from django.http import HttpResponse, JsonResponse

# Create your views here.

# API_URL = 'https://api.stackexchange.com/2.3/search/advanced?order=desc&sort=activity&q=python&body=python%20pandas&site=stackoverflow'
API_URL = "https://api.stackexchange.com/2.3/search/advanced?"


def index(request):
    data = ""
    is_cached = False
    body = ''
    title = ''
    q = ''
    page_number = 0
    if request.method == "POST":
        body = request.POST.get('body')
        title = request.POST.get('title')
        q = request.POST.get('q')
        page_number = 1

        session_key = body+title+q
        is_cached = (session_key in request.session)

        if not is_cached:
            data = make_api_request(body, title, q, page_number)
            request.session[session_key] = data
        data = request.session[session_key]

    context = {'data': data, 'is_cached': is_cached,
               'body': body, 'title': title, 'q': q, 'page': page_number}
    return render(request, 'index.html', context=context)


def make_api_request(body, title, q, page_number):
    make_url = f'{API_URL}q={q}&page={page_number}&body={body}&title={title}&site=stackoverflow'
    print(make_url)
    response = requests.get(make_url)
    data = response.json()
    return data


def load_more(request):
    data = ""
    is_cached = False
    page = 0
    body = request.GET.get('body')
    title = request.GET.get('title')
    q = request.GET.get('q')
    page = request.GET.get('page')
    session_key = body+title+q+str(page)
    page = int(page) + 1
    is_cached = (session_key in request.session)
    if not is_cached:
        data = make_api_request(body, title, q, page)
        request.session[session_key] = data
    data = request.session[session_key]
    response = {'data': data, 'page': page,
                'is_cached': is_cached, 'has_more': data['has_more']}
    return JsonResponse(data=response)
