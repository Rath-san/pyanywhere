from django import template
from wagtail.core.models import Page
# Library.assignment_tag = Library.simple_tag
register = template.Library()


@register.assignment_tag(takes_context=True)
def get_site_root(context):
    return context['request'].site.root_page


def has_menu_children(page):
    return page.get_children().live().in_menu().exists()


@register.inclusion_tag('modules/top_menu.html', takes_context=True)
def top_menu(context, parent, calling_page=None):
    menuitems = parent.get_children().filter(
        live=True,
        show_in_menus=True
    )

    for menuitem in menuitems:
        menuitem.show_dropdown = has_menu_children(menuitem)
        menuitem.active = (
            calling_page.path.startswith(menuitem.path) if calling_page else False
        )
    return {
        'calling_page': calling_page,
        'menuitems': menuitems,
        'home': parent,
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
    }

@register.inclusion_tag('modules/side_menu.html', takes_context=True)
def side_menu(context, parent, shallow=False, calling_page=None):
    menuitems = parent.get_children().filter(
        live=True,
        # show_in_menus=True
    )
    for menuitem in menuitems:
        menuitem.show_dropdown = has_menu_children(menuitem)
        menuitem.children = menuitem.get_children().live()
        for child in menuitem.children:
            child.active = (
                calling_page.path.startswith(child.path) if calling_page else False
            )
        menuitem.shallow = shallow
        menuitem.active = (
            calling_page.path.startswith(menuitem.path) if calling_page else False
        )
    return {
        'calling_page': calling_page,
        'menuitems': menuitems,
        'home': parent,
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
    }


@register.inclusion_tag('modules/top_menu_children.html', takes_context=True)
def top_menu_children(context, parent):
    menuitems_children = parent.get_children()
    menuitems_children = menuitems_children.live().in_menu()
    return {
        'parent': parent,
        'menuitems_children': menuitems_children,
        # required by the pageurl tag that we want to use within this template
        'request': context['request'],
    }


# @register.inclusion_tag('modules/sub_menu.html', takes_context=True)
# def sub_menu(context, calling_page=None):
#     self = context.get('self')
#     siblings = self.get_siblings().live().in_menu()
#     return {
#         'parent': self.get_parent(),
#         'siblings': siblings,
#         'request': context['request'],
#         'calling_page': calling_page,
#     }


# @register.inclusion_tag('modules/breadcrumbs.html', takes_context=True)
# def breadcrumbs(context):
#     self = context.get('self')
#     if self is None or self.depth <= 2:
#         # When on the home page, displaying breadcrumbs is irrelevant.
#         ancestors = ()
#     else:
#         ancestors = Page.objects.ancestor_of(
#             self, inclusive=True).filter(depth__gt=2)
#     return {
#         'ancestors': ancestors,
#         'request': context['request'],
#     }
