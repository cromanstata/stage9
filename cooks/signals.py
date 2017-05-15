from django.dispatch import Signal

favorite_created = Signal(providing_args=['favorer'])
favorite_removed = Signal(providing_args=['favorer'])
favorer_created = Signal(providing_args=['recipe'])
favorer_removed = Signal(providing_args=['recipe'])
favorite_recipe_created = Signal(providing_args=['favorers'])
favorite_recipe_removed = Signal(providing_args=['favorers'])