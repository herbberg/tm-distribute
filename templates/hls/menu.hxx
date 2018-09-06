{% extends "header.hxx" %}
{% block code %}
#ifndef impl_menu_h
#define impl_menu_h

#include "../impl/conditions.hxx"
#include "../impl/seeds.hxx"

#define IMPL_MENU_NAME "{{ menu.name }}"
#define IMPL_MENU_UUID "{{ menu.uuid }}"
#define IMPL_DIST_UUID "{{ menu.dist_uuid }}"

namespace impl {
namespace menu {

} // namespace menu
} // namespace impl

#endif
{% endblock code %}
