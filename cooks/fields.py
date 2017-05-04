from django.utils.translation import ugettext_lazy as _

# Constants for all available difficulty types.
SIMPLE = "simple"
MEDIUM = "medium"
DIFFICULT = "difficult"

# Names for all available difficulty types.
DIFFICULTIES = (
    (SIMPLE, _("simple")),
    (MEDIUM, _("medium")),
    (DIFFICULT, _("difficult")),
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
