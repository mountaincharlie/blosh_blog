from django.db import models
from django.contrib.auth.models import User  # model for a user
from cloudinary.models import CloudinaryField  # getting CloudinaryField type

# blog post status tuple
BLOG_STATUS = ((0, 'Draft'), (1, 'Published'))

# Blog table in the db inheriting the Model class
class Blog(models.Model):
    title = models.CharField(max_length=200, unique=True)
    # uses User model, cascade=>deletes all posts if author deleted
    # related_name=>way to refer to it e.g. author.blog_posts
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    content = models.TextField()
    # spcifying media type and default
    main_image = CloudinaryField('image', default='placeholder')
    # shown on homepage tile
    summary = models.TextField()
    # allowing it to be blank
    likes = models.ManyToManyField(User, blank=True, related_name='blog_likes')
    comments = models.ManyToManyField(User, blank=True, related_name='blog_comments')
    slug = models.SlugField(max_length=200, unique=True)
    # setting choices and default
    status = models.IntegerField(choices=BLOG_STATUS, default=0)

    class Meta:
        # setting blolgs to be ordered by newest created date
        ordering = ['-created_date']
    
    def __str__(self):
        # returns string rep of how the table is displayed
        return self.title
    
    def number_of_likes(self):
        # returns total number of likes
        return self.likes.count()
    
    def number_of_comments(self):
        # returns total number of comments
        return self.comments.count()


class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comment')
    # not unique so users can comment more than once
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    # boolean field for if the comment is approved or not
    approved = models.BooleanField(default=False)

    class Meta:
        # setting blolgs to be ordered by newest created date
        ordering = ['-created_date']
    
    def __str__(self):
        # returns string rep of how the table is displayed
        return f"Comment: {self.body} by: {self.name}"
