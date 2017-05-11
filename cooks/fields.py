from django.utils.translation import ugettext_lazy as _

# Constants for all available cuisine types.
ASIAN = "asian"
CARIBBEAN = "caribbean"
CHINESE = "chinese"
FRENCH = "french"
RUSSIAN = "russian"
INDIAN = "indian"
ITALIAN = "italian"
MEXICAN = "mexican"
MEDITERRANEAN = "mediterranean"

# Names for all available cuisine types.
CUISINE = (
    (ASIAN, _("Asian")),
    (CARIBBEAN, _("Caribbean")),
    (CHINESE, _("Chinese")),
    (FRENCH, _("French")),
    (RUSSIAN, _("Russian")),
    (INDIAN, _("Indian")),
    (ITALIAN, _("Italian")),
    (MEXICAN, _("Mexican")),
    (MEDITERRANEAN, _("Mediterranean")),
)

# Constants for all available meal types.
BREAKFAST = "breakfast"
DINNER = "dinner"
QUICK = "quick"
SOUPS = "soups"
DESSERTS = "desserts"
FISH = "fish"
GRILL = "grill"
KIDS = "kids"
CHICKEN = "chicken"
MEAT = "meat",
SALADS = "salads"
VEGGIE = "veggie"
SEAFOOD = "seafood"

# Names for all available meal types.
MEALTYPE = (
    (BREAKFAST, _("Breakfast")),
    (DINNER, _("Dinner")),
    (QUICK, _("Quick & Easy")),
    (SOUPS, _("Soups")),
    (DESSERTS, _("Desserts")),
    (FISH, _("Fish")),
    (GRILL, _("Grill")),
    (KIDS, _("Kids")),
    (CHICKEN, _("Chicken")),
    (MEAT, _("Meat")),
    (SALADS, _("Salads")),
    (VEGGIE, _("Veggie")),
    (SEAFOOD, _("Seafood")),
)


# Constants for all available difficulty types.
SIMPLE = "simple"
MEDIUM = "medium"
DIFFICULT = "difficult"

# Names for all available difficulty types.
DIFFICULTIES = (
    (SIMPLE, _("Simple")),
    (MEDIUM, _("Medium")),
    (DIFFICULT, _("Difficult")),
)

# Constants for all available unit types.
LITER = "liter"
KG = "kg"
GRAM = "gram"
CUP = "cup"
TSPOON = "tspoon"
SPOON = "spoon"


# Names for all available unit types.
UNITS = (
    (CUP, _("cup")),
    (KG, _("kg")),
    (LITER, _("liter")),
    (GRAM, _("gram")),
    (TSPOON, _("tspoon")),
    (SPOON, _("spoon")),
)
