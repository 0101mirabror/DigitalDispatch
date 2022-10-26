import json
from django.db.models import Q
from django.http import JsonResponse
from django.http.response import HttpResponse, Http404, HttpResponseRedirect
from core.models import GeneralLink, Section, LinkType, Company, Like
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.utils.text import slugify
from django.views.decorators.csrf import csrf_exempt
from users.models import BookmarkedLink
from core.forms import GeneralLinkForm

def link_list(request, slug, type_slug=None):
    
    section = get_object_or_404(Section, slug=slug) # slug=areas -> Section=Sohalar
    # links = GeneralLink.objects.filter(section=section)
    links = section.generallink_set.all()
    linktypes = section.linktype_set.all()
    filter_options = GeneralLink.objects.filter(
        Q(section__slug='areas') | Q(section__slug='tools'))
    # filter_options = GeneralLink.objects.filter(section__slug = 'areas')
    # filter_options = GeneralLink.objects.filter(section__slug = 'tools')
    choosen_filter = request.GET.get('filter')

    print(request.GET)
    if choosen_filter:
        link = GeneralLink.objects.filter(slug=choosen_filter).first()
        if link:
            links = links.filter(tools__in=[link])
    # print(request.query_params)
    sort = request.GET.get('sort')
    if sort in ('name', '-name', '-created_time', '-rating'):
        links = links.order_by(sort)
    page = int(request.GET.get('page', 1)) # har bir page da 10tadan link chiqsin
    format = request.GET.get('format', 'html')
    links = links[(page-1)*3:page*3]  # page=1 -> links[0:10] | page=2  -> links[10:20]  
    context = {
        'section': section, 
        'links': links,
        'linktypes': linktypes,
        'filter_options': filter_options,
        'slug': slug
    }
    
    if type_slug:
        type = get_object_or_404(LinkType, slug=type_slug)
        links = links.filter(type=type)
        if sort in ('name', '-name', '-created_time', '-rating'):
            links = links.order_by(sort)
        context['links'] = links
        context['type_slug'] = type_slug
        
    if format == 'json':
       print('returned json')
       return JsonResponse(data={
           'links': [{
               'id': link.id,
               'photo_url': link.photo.url,
               'name': link.name
               # ...
           } for link in links],   # [{....} for link in links]
           'page': page
       })
    # {'links': [], 'page': 1}   

    return render(request, "link_list.html", context) # shortcuts


# def link_detail(request,link_slug):
#     try:
#         link = GeneralLink.objects.get(slug=link_slug)  # get(name="birinchi havola")
#     except Exception as e:
#         print(e)
#         raise Http404('Afsuski siz izlagan link topilmadi!')
#         # return HttpResponse("Afsuski siz izlagan link topilmadi!") # 200 HTTP 
    

#     return render(request, 'link_detail.html', {'link': link}) # 200 HTTP


def link_detail(request, link_slug):
    link = get_object_or_404(GeneralLink, slug=link_slug) # shortcut
       
    link.views_count += 1
    link.save()
    return render(request, 'link_detail.html', {'link': link}) # 200 HTTP


# # def link_create(request):
#     errors = {}
#     data = {}
#     print(f"==========={request.method}===============")
#     if request.method == 'GET':
#         print('bu GET so\'rovi edi. Bunday zaproslar kelganda biror logika boyicha response qaytarish mumkin')
#         print('request.GET=', request.GET) # request.GET  - QueryDict: {} (QueryDictionary)

#     if request.method == 'POST':
#         print(request.POST)
#         link_name = request.POST.get('name')
#         link_description = request.POST.get('description')
#         link_url = request.POST.get('url')
#         data['name'] = link_name
#         data['description'] = link_description
#         data['url'] = link_url
#         # new_link = Link(name=link_name)
#         # new_link.url = link_url
#         # new_link.description = link_description
#         # new_link.image = 'asd'
#         # new_link.save()
#         if link_name and link_url:
#             old_link = Link.objects.filter(name=link_name) # QuerySet [<Link 1>, <Link 2>]
#             if old_link: # old_link.exists()
#                 errors['other'] = 'Bunday nom bilan havola qoshilgan. Iltimos boshqa nom tanlang'
            
#             new_link = Link.objects.create(
#                 name=link_name,
#                 description=link_description,
#                 url=link_url
#             )
#             return redirect('/havolalar/') # domain.nomie/havolalar/
#         else:
#             if not link_name:
#                 errors['name'] = 'Please input link name'
            
#             if not link_url:
#                 errors['url'] = 'Please input link url'

#     return render(request, 'link_create.html', {'errors': errors, 'data': data}) # 200 HTTP

def link_create(request):
    form = GeneralLinkForm( data=request.POST or None, files=request.FILES or None)
    context = {
        'sections': Section.objects.all(),
        'types': LinkType.objects.all(),
        'form': form,
        'tools': GeneralLink.objects.filter(Q(section__slug="areas") | Q(section__slug="tools")),
        'companies': Company.objects.all()
    }
    if request.method == 'POST':
        print(request.POST)
        if form.is_valid(): # False

            new_link = form.save(commit=False) # model from
            new_link.author = request.user
            new_link.slug = slugify(new_link.name)
            print('SALOM', new_link)
            new_link.save()
            return redirect('/')
    print(form.errors)
    return render(request, 'link_create.html', context) # 200 HTTP

@csrf_exempt
def like(request):
    if not request.user.is_authenticated:
        return HttpResponse(status=401)
    if request.method =="POST":
        print('post request recieved')
        print(request.POST)
        print("123AAAAAAAAAAAAB",request.body)
        try:
            data = json.loads(request.body)
            print(data)
            obj_type = data['obj_type']
            obj_id = int(data['id'])
            value = data['value']
            #obj_type = request.POST.get('obj_type')
            #obj_id = request.POST.get('id')
            #value = request.POST['value']
            #request.user
            # like object
            if obj_type == 'link':
                old_like = Like.objects.filter(author = request.user, link=obj_id).first()
                if old_like:
                    if old_like.type  == value:
                        old_like.delete()
                    else:
                        old_like.type = value
                        old_like.save()
                else:
                    Like.objects.create(
                        author = request.user,
                        link_id = obj_id,
                        type = value
                    )
            return HttpResponse(status=200)

        except Exception as e:
            print(e)
            pass
            return HttpResponse(status=400)
    return HttpResponse(status=403)



@csrf_exempt
def bookmarking(request, link_id):
    if not request.user.is_authenticated:
        return HttpResponse(status=401)
    if request.method == 'POST':
        try:
            data = json.loads(request.body)   # json.loads: str or bytes --> dict 
            status = data['status']
            obj_id = link_id
            bookmark, created = BookmarkedLink.objects.get_or_create(user=request.user, link_id=obj_id) # -> (bookmark obj, True/False)
            bookmark.status = status
            bookmark.save()
            return HttpResponse(status=200)
        except Exception as e:
            print(e)
            return HttpResponse(status=400)
    return HttpResponse(status=403)


# def link_update(request, link_id):
#     link = get_object_or_404(Link, id=link_id)
#     form = LinkForm(instance=link) #
    
#     if request.method == 'POST':
#         form = LinkForm(instance=link, data=request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('/havolalar/') # domain.nomie/havolalar/

#     return render(request, 'link_update.html', {'form': form})
