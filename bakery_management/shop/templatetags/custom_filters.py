from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    # Check if the field is a form field instance
    if hasattr(field, 'as_widget'):
        return field.as_widget(attrs={'class': css_class})
    return field  # Return the field as-is if it’s not a form field