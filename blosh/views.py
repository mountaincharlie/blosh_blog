from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from .models import Blog, Comment

# Creating generic/reausable views with classes

# list of blogs
class BlogList(generic.ListView):
    # table model to use
    model = Blog
    # getting all the 'Published' status posts in date order
    queryset = Blog.objects.filter(status=1).order_by('-created_date')
    template_name = 'index.html'
    # number of posts to display per page
    paginate_by = 8

# viewing a blog
class BlogView(View):
    # using GET method to get the blog from db
    # including standard arguments and keyword args
    def get(self, request, slug, *args, **kwargs):
        queryset = Blog.objects.filter(status=1)  # all published blogs
        blog = get_object_or_404(queryset, slug=slug)  # blog with its slug

        # getting all the approved comments in date order
        comments = Comment.objects.filter(approved=True).order_by('created_date')
        # boolean value for if the user liked this post or not
        liked = False
        # checking if the specific user liked it (using user.id)
        if blog.likes.filter(id=self.request.user.id).exists():
            liked = True

        # sending all this info to the render method
        return render(
            request,
            "blog_view.html",  # required template
            # dictionary with the context (data to be passed to template)
            {
                "blog": blog,
                "comments": comments,
                "commented": False,  # until comments are approved
                "liked": liked,
                # "comment_form": CommentForm()
            },
        )

    # POST method to add
    # getting date from comment_form
    # checking if a comment has been made (is True)
    # sending all this info to the render method
