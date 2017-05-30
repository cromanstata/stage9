from django.dispatch import Signal

comment_recipe_created = Signal(providing_args=['recipe', 'comment'])
rating_recipe_created = Signal(providing_args=['recipe', 'rating'])
