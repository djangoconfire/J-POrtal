from django import template

register=template.Library()

@register.filter(name='get_item_from_dict')
def get_item_from_dict(dictionary,key):
	return dictionary.get(key)


