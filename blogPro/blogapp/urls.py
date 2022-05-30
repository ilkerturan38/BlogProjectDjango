from django.contrib import admin
from django.urls import path,include
from .import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index,name="index"),
    path('contact',views.contact,name="contact"),

    path('about',views.about,name="about"),
    path('aboutList',views.aboutList,name="aboutList"),
    path('aboutInsert',views.aboutInsert,name="aboutInsert"),
    path('aboutUpdate/<int:id>',views.aboutUpdate,name="aboutUpdate"),

    path('authorBlog/<int:id>',views.authorBlog,name="authorBlog"),
    path('AuthorBlogStatusUpdateFalse/<int:id>',views.AuthorBlogStatusUpdateFalse,name="AuthorBlogStatusUpdateFalse"),
    path('AuthorBlogStatusUpdateTrue/<int:id>',views.AuthorBlogStatusUpdateTrue,name="AuthorBlogStatusUpdateTrue"),

    path('blogComment/<int:id>',views.blogComment,name="blogComment"),

    path('authorList/',views.authorList,name="authorList"),
    path('authorInsert/',views.authorInsert,name="authorInsert"),
    path('authorUpdate/<int:id>',views.authorUpdate,name="authorUpdate"),
    path('authorDelete/<int:id>',views.authorDelete,name="authorDelete"),
    path('authorStatusUpdateTrue/<int:id>',views.authorStatusUpdateTrue,name="authorStatusUpdateTrue"),
    path('authorStatusUpdateFalse/<int:id>',views.authorStatusUpdateFalse,name="authorStatusUpdateFalse"),
    
    path('categoryBlogList/<slug:slug>',views.categoryBlogList,name="categoryBlogList"),
    path('categoryList/',views.categoryList,name="categoryList"),
    path('categoryInsert/',views.categoryInsert,name="categoryInsert"),
    path('categoryUpdate/<int:id>',views.categoryUpdate,name="categoryUpdate"),
    path('categoryDelete/<int:id>',views.categoryDelete,name="categoryDelete"),
    path('categoryStatusUpdateTrue/<int:id>',views.categoryStatusUpdateTrue,name="categoryStatusUpdateTrue"),
    path('categoryStatusUpdateFalse/<int:id>',views.categoryStatusUpdateFalse,name="categoryStatusUpdateFalse"),

    path('blogDetails/<int:id>',views.blogDetails,name="blogDetails"),
    path('blogList/',views.blogList,name="blogList"),
    path('blogInsert/',views.blogInsert,name="blogInsert"),
    path('blogUpdate/<int:id>',views.blogUpdate,name="blogUpdate"),
    path('blogDelete/<int:id>',views.blogDelete,name="blogDelete"),
    path('BlogStatusUpdateFalse/<int:id>',views.BlogStatusUpdateFalse,name="BlogStatusUpdateFalse"),
    path('BlogStatusUpdateTrue/<int:id>',views.BlogStatusUpdateTrue,name="BlogStatusUpdateTrue"),

    path('search',views.search,name="search"),

    path('commentList',views.commentList,name="commentList"),
    path('commentInsert/<int:id>',views.commentInsert,name="commentInsert")
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
