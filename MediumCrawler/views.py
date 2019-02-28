from django.shortcuts import render, redirect
from bs4 import BeautifulSoup
from .models import Blog, AccessedTag, BlogTag
from .forms import tag_search_form
from .blog_crawler import blog_crawler
import requests

def home_page(request):
    context = {}
    if request.method == "POST":
        submitted_tag = tag_search_form(request.POST)
        if submitted_tag.is_valid():
            current_tag = AccessedTag(tag_name = request.POST["tag_name"])
            current_tag.save()
            url = "https://medium.com/tag/" + request.POST["tag_name"]
            blogs_data = requests.get(url).text
            soup = BeautifulSoup(blogs_data, "html.parser")
            
            for each_div in soup.find_all("div", { "class" : "postArticle-readMore" }):
                if each_div is not None:
                    blog_info = blog_crawler(each_div.find("a")["href"])
                    current_blog = Blog(blog_url = blog_info.url,
                                        blog_author = blog_info.author,
                                        blog_title = blog_info.blog_title,
                                        blog_published_on = blog_info.date_published,
                                        blog_modified_on = blog_info.date_modified,
                                        blog_read_duration = blog_info.article_duration)
                    current_blog.save()
                    for tag in blog_info.blog_tags:
                        current_blog_tag = BlogTag(tag_name = tag)
                        current_blog_tag.save()
                        current_blog.blog_tags.add(current_blog_tag)
                    current_tag.blogs.add(current_blog)

            return redirect("tag/" + current_tag.tag_name)
        else:
            return redirect("home_page")
    context["form"] = tag_search_form
    return render(request, "MediumCrawler/home_page.html", context)

def tag_page(request, pk):
    context = {}
    context["tag_data"] = AccessedTag.objects.get(tag_name = pk)
    return render(request, "MediumCrawler/tag_page.html", context)

def search_history(request):
    context = {}
    context["accessed_tags"] = AccessedTag.objects.all()
    return render(request, "MediumCrawler/search_history.html", context)
