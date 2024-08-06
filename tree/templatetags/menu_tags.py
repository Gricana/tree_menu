from django import template
from tree.models import MenuItem

register = template.Library()


@register.inclusion_tag('menu/init_menu.html', takes_context=True)
def draw_menu(context, menu_name):
    """
    This function generates a menu based on the provided menu name and the current request.
    It retrieves the menu items from DB, identifies the active item based on the current URL,
    and prepares the necessary data for rendering the menu template.

    Parameters:
    context (dict): The context dictionary provided by Django's template system.
    menu_name (str): The name of the menu to be displayed.

    Returns:
    dict: A dict containing the keys:
        - menu_items: A list of root menu items.
        - active_item: The currently active menu item (or None if no active item is found).
        - active_item_ancestors: A list of ancestors of the active item (or empty list if no active item is found).
        - active_item_children: A list of children of the active item (or empty list if no active item is found).
        - request: The current request object.
    """
    request = context['request']
    current_url = request.path

    items = MenuItem.objects.filter(menu__name=menu_name).select_related('parent').prefetch_related('children')

    if not items.exists():
        return {'menu_items': [], 'active_item': None}

    root_items = [item for item in items if item.parent is None]
    active_item = get_active_item(items, current_url)
    active_item_ancestors = get_ancestors(active_item) if active_item else []
    active_item_children = active_item.children.all() if active_item else []

    return {
        'menu_items': root_items,
        'active_item': active_item,
        'active_item_ancestors': active_item_ancestors,
        'active_item_children': active_item_children,
        'request': request
    }


def get_active_item(items, current_url):
    """
    This function identifies the active menu item based on the provided list of menu items and the current URL.

    Parameters:
    items (list): A list of MenuItem objects representing the menu items.
    current_url (str): The URL of the current request.

    Returns:
    MenuItem or None: The active menu item if found, otherwise None.
    """
    for item in items:
        if item.get_absolute_url() == current_url:
            return item
    return None


def get_ancestors(item):
    """
    This function retrieves the ancestors of a given menu item.

    Parameters:
    item (MenuItem): The menu item for which to retrieve the ancestors.
        The MenuItem object should have a 'parent' attribute representing its parent menu item.

    Returns:
    list: A list of MenuItem objects representing the ancestors of the given item.
    """
    ancestors = []
    while item:
        ancestors.append(item)
        item = item.parent
    return ancestors
