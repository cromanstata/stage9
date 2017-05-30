from django import template
from comments.models import Like, Comment
from comments.forms import CommentForm
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.template import Node, TemplateSyntaxError


register = template.Library()

@register.simple_tag(name='can_rate')
def has_rated(object, user):
    """ returns boolean for if a user already rated a recipe """
    ratings = Comment.objects.filter(object_id=object.id, user_id=user.id)
    ratings = ratings.exclude(rating=None)
    if ratings:
        return False
    else:
        return True


@register.simple_tag(name='get_model_name')
def get_model_name(object):
    """ returns the model name of an object """
    return type(object).__name__


@register.simple_tag(name='get_app_name')
def get_app_name(object):
    """ returns the app name of an object """
    return type(object)._meta.app_label


@register.tag(name='mkrange')
def mkrange(parser, token):
    """
    Accepts the same arguments as the 'range' builtin and creates
    a list containing the result of 'range'.

    Syntax:
        {% mkrange [start,] stop[, step] as context_name %}

    For example:
        {% mkrange 5 10 2 as some_range %}
        {% for i in some_range %}
          {{ i }}: Something I want to repeat\n
        {% endfor %}

    Produces:
        5: Something I want to repeat
        7: Something I want to repeat
        9: Something I want to repeat
    """

    tokens = token.split_contents()
    fnctl = tokens.pop(0)

    range_args = []
    while True:
        token = tokens.pop(0)

        if token == "as":
            break

        range_args.append(int(token))

    context_name = tokens.pop()

    return RangeNode(range_args, context_name)


class RangeNode(Node):
    def __init__(self, range_args, context_name):
        self.range_args = range_args
        self.context_name = context_name

    def render(self, context):
        context[self.context_name] = range(*self.range_args)
        return ""


@register.simple_tag(name='get_rating')
def get_rating(object):
    # the avarge rating for the recipe
    try:
        ratings = Comment.objects.filter(object_id=object.id)
        ratings = ratings.exclude(rating=None)
        rating_count = 0
        rating_sum = 0
        for rating in ratings:
            rating_sum += rating.rating
            rating_count += 1
        if rating_count==0:
            return ("No rating")
        else:
            return round(rating_sum / rating_count * 2) / 2

    except ObjectDoesNotExist:
        # recipe = Recipe.objects.get(id=recipe)
        # likes = Like(recipe=recipe, likes_count=0, updated=timezone.now())
        # likes.save()
        # return likes
        print("no ratings for this recipe")
        rating_avg = 0
        return rating_avg


@register.simple_tag(name='get_comment_count')
def get_comment_count(object):
    """ returns the count of comments of an object """
    model_object = type(object).objects.get(id=object.id)
    return model_object.comments.all().count()


def get_comments(object, user):
    """
    Retrieves list of comments related to a certain object and renders
    The appropriate template to view it
    """
    model_object = type(object).objects.get(id=object.id)
    comments = model_object.comments.all()
    liked = []
    for comment in comments:
        try:
            Like.objects.get(user=user, comment=comment)
            liked.append(True)
        except:
            liked.append(False)
    return {"form": CommentForm(),
            "comment_liked": zip(comments, liked),
            "target": object,
            "user": user,
            "comments_count": comments.count(),
            "allow_likes": getattr(
                settings,
                'COMMENTS_ALLOW_LIKES',
                True)}

register.inclusion_tag('comments/comments.html')(get_comments)


def comment_form(object, user):
    """
    renders template of comment form
    """
    return {"form": CommentForm(),
            "target": object,
            "user": user,
            "allow_anonymous": getattr(
                settings,
                'COMMENTS_ALLOW_ANONYMOUS',
                False)}


register.inclusion_tag('comments/comment_form.html')(comment_form)


