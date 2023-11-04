from django import template
from django.urls import resolve
from ..models import MenuItem

register = template.Library()


@register.filter
def keyval(dictionary, key):
    if key in dictionary.keys():
        return dictionary[key]


@register.inclusion_tag('menu_tags/menu.html', takes_context=True)
def show_menu(context, menu_name):
    current_url = context['request'].path
    resolved_url = resolve(current_url).url_name

    def find_by_id(id, items_list):
        return next(filter(lambda item: item['id'] == id, items_list), None)

    all_menu_items = MenuItem.objects.filter(menu__name=menu_name).values()

    current_item = next(filter(lambda item: item['url'] in [current_url, resolved_url], all_menu_items), None)
    root_level_items = list(filter(lambda item: item['parent_id'] is None, all_menu_items))

    if current_item:
        # Get ids for all parents of current item (included)
        parent_ids = [current_item['id']]
        next_parent = find_by_id(current_item['parent_id'], all_menu_items)
        while next_parent:
            parent_ids.append(next_parent['id'])
            next_parent = find_by_id(next_parent['parent_id'], all_menu_items)

        # Filter all menu items to rendered only
        filtered_items = []
        for item in all_menu_items:
            if item['parent_id'] in parent_ids or item['parent_id'] is None:
                filtered_items.append(item)

        # Make dict with child items for every shown item
        children = {}
        for item in filtered_items:
            children[item['id']] = list(filter(lambda child: child['parent_id'] == item['id'], filtered_items))
    else:
        children = {}

    return {
        'menu': root_level_items,
        'children': children,
        'current_item': current_item,
    }
