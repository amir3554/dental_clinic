from django import template
from dental_clinic_project import settings

register = template.Library()


# This filter takes a numeric value and returns it formatted as a currency string with 2 decimal places.
@register.filter(name='currency')
def currency(value):
    try:
        # Convert to float first if it's a string
        numeric_value = float(value) if isinstance(value, int) else value
        return f"{numeric_value:.2f} {settings.CURRENCY}"
    except (ValueError, TypeError):
        # Return original if conversion fails
        return value
    


