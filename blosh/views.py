from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from .models import Blog  # , Comment
from .forms import CommentForm  # our form class
from django.http import HttpResponseRedirect

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
    # getting blog from the db
    def get(self, request, slug, *args, **kwargs):
        queryset = Blog.objects.filter(status=1)  # all published blogs
        blog = get_object_or_404(queryset, slug=slug)

        # getting all the approved comments in date order
        # where blog is in the Comment table and has related name = 'comments'
        comments = blog.comments.filter(approved=True).order_by('-created_date')

        # boolean value for if the user liked this post or not
        liked = False
        # checking if the specific user liked it (using user.id)
        if blog.likes.filter(id=self.request.user.id).exists():
            liked = True

        # sending all this info to the render method
        return render(
            request,
            "blog_view.html",  # required template
            # context as dictionary of data to be passed to template
            {
                "blog": blog,
                "comments": comments,
                "commented": False,  # until comment made
                "liked": liked,
                "comment_form": CommentForm()
            },
        )

    # post method only for authnticated users (v similar to get method)
    def post(self, request, slug, *args, **kwargs):
        queryset = Blog.objects.filter(status=1)
        blog = get_object_or_404(queryset, slug=slug)
        comments = blog.comments.filter(approved=True).order_by('created_date')
        liked = False
        if blog.likes.filter(id=self.request.user.id).exists():
            liked = True

        # getting the form data
        comment_form = CommentForm(data=request.POST)
        # checking if comment_form is True
        if comment_form.is_valid():
            # getting the users email and username
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.blog = blog  # specify the blog it belongs to
            comment.save()
        else:
            comment_form = CommentForm()  # empty instance

        return render(
            request,
            "blog_view.html",
            {
                "blog": blog,
                "comments": comments,
                "commented": True,
                "liked": liked,
                "comment_form": comment_form  # not calling the function again
            },
        )

# liking blogs
class BlogLike(View):

    # when the user clicks on the like button
    def post(self, request, slug):
        # getting the blog post
        blog = get_object_or_404(Blog, slug=slug)
        # if the user is logged in, clicking will toggle like/unlike
        if blog.likes.filter(id=request.user.id).exists():
            blog.likes.remove(request.user)
        else:
            blog.likes.add(request.user)

        # now want the template to refresh to show the change
        return HttpResponseRedirect(reverse('blog_view', args=[slug]))
