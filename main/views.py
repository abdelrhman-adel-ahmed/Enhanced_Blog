from django.shortcuts import render,get_object_or_404
from .models import Post,Author,PostView,Category
from marketing.models import Signup
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.db.models import Count,Q
from .forms import CommentForm,PostForm
from django.shortcuts import HttpResponseRedirect,reverse,redirect

#count each category posts  
def get_categoty_count():
    queryset=Post.objects.values('category__title').annotate(Count('category__title'))
    return queryset

def get_author(user):
    qs=Author.objects.filter(user=user)
    print(qs)
    print(qs[0])
    if qs.exists():
        return qs[0]
    else:
        return None 

def home(request):
    posts=Post.objects.filter(featured=True)
    latest=Post.objects.order_by('-timestamp')[:3]

    if request.method=='POST':
        print(request.POST)
        email=request.POST['email']
        new_signup=Signup()
        new_signup.email=email
        new_signup.save()

    context={
        'posts':posts,
        'latest':latest
    }
    return render(request,"index.html",context)

def blog(request):
    posts=Post.objects.all()
    latest=Post.objects.order_by('-timestamp')[:3]
    category_count=get_categoty_count()
    paginator=Paginator(posts,3)
    page_request_var='page'
    page=request.GET.get(page_request_var)
    try:
        paginted_queryset=paginator.page(page)
        #if not an integer (and if the key is not what we specified e.x ?ali=2)
    except PageNotAnInteger:
        paginted_queryset=paginator.page(1)
    except EmptyPage:
        paginted_queryset=paginator.page(paginator.num_pages)

    context={
        'paginated_queryset':paginted_queryset,
        'page_request_var':page_request_var,
        'most_recent':latest,
        'category_count':category_count,
    }
    return render(request,"blog.html",context)

def post(request,id):
    category_count=get_categoty_count()
    latest=Post.objects.order_by('-timestamp')[:3]
    post=get_object_or_404(Post,id=id)
    PostView.objects.get_or_create(user=request.user,post=post) 
    form=CommentForm(request.POST or None)
    if request.method=="POST":
        if form.is_valid():
            form.instance.user=request.user
            form.instance.post=post
            form.save()
        return HttpResponseRedirect(post.get_absolute_url())
    #may be some post doesnot have prev or next 
    try:
        next_post=post.get_next_by_timestamp()
    except:
        next_post=None
    try:
        prev_post=post.get_previous_by_timestamp()
    except:
        prev_post=None
    context={
        'post':post,
        'category_count':category_count,
        'most_recent':latest,
        'next_post':next_post,
        'prev_post':prev_post,
        'form':form
    }  
    return render(request,"post.html",context)

def about(request):
    return render(request,'about.html')

def get_blog_query_post(query=None):
    posts=Post.objects.all()
    queryset=posts.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        ).distinct()
    print(queryset)
    return queryset
    
def search(request):
    posts=Post.objects.all()
    #if no value bassed for seatch set deffult of nothing search=""
    context={}
    query=""
    if request.GET:
        query=request.GET.get('search','')
        context['query']=str(query)
    queryset=get_blog_query_post(query)
    latest=Post.objects.order_by('-timestamp')[:3]
    category_count=get_categoty_count()
    paginator=Paginator(queryset,3)
    #page_request_var='page'
    page=request.GET.get('page',1)
    try:
        paginted_queryset=paginator.page(page)
        #if not an integer (and if the key is not what we specified e.x ?ali=2)
    except PageNotAnInteger:
        paginted_queryset=paginator.page(1)
    except EmptyPage:
        paginted_queryset=paginator.page(paginator.num_pages)

    context={
        'query':query,
        'paginated_queryset':paginted_queryset,
        'most_recent':latest,
        'category_count':category_count,
    }
    return render(request,"search.html",context)


def post_create(request):
    title='Create an article'
    form=PostForm(request.POST or None,request.FILES or None)
    author=get_author(request.user)
    if request.method== 'POST':
        if form.is_valid():
            form.instance.author=author
            form.save()
            return HttpResponseRedirect(form.instance.get_absolute_url())
            #return redirect(reverse('post',kwargs={'id':form.instance.id}))
    context={
        'form':form,
        'title':title
    }
    return render(request, 'post_create.html',context)



def post_delete(request,id):
    post=get_object_or_404(Post,id=id)
    post.delete()
    return redirect(reverse('blog'))

def post_update(request,id):
    title='Update an article'
    post=get_object_or_404(Post,id=id)
    form=PostForm(request.POST or None,request.FILES or None,instance=post)
    author=get_author(request.user)
    if request.method== 'POST':
        if form.is_valid():
            form.instance.author=author
            form.save()
            return HttpResponseRedirect(form.instance.get_absolute_url())
    context={
        'form':form,
        'title':title
    }
    return render(request, 'post_create.html',context)

def post_by_tag(request,tag):
    tag_query=Category.objects.get(title=tag)
    tag_id=tag_query.id
    posts=Post.objects.filter(category=tag_id)
    latest=Post.objects.order_by('-timestamp')[:3]
    category_count=get_categoty_count()
    paginator=Paginator(posts,3)
    page_request_var='page'
    page=request.GET.get(page_request_var)
    try:
        paginted_queryset=paginator.page(page)
        #if not an integer (and if the key is not what we specified e.x ?ali=2)
    except PageNotAnInteger:
        paginted_queryset=paginator.page(1)
    except EmptyPage:
        paginted_queryset=paginator.page(paginator.num_pages)

    context={
        'paginated_queryset':paginted_queryset,
        'page_request_var':page_request_var,
        'most_recent':latest,
        'category_count':category_count,
    }
    return render(request,"posts_by_tag.html",context)


