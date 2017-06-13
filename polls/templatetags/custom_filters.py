from django.template.defaulttags import register

@register.filter
def get_dict_value_for_key(dictionary, key):
    return dictionary.get(key)