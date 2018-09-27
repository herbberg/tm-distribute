{% extends "header.hxx" %}
{% block code %}
#ifndef impl_cuts_h
#define impl_cuts_h

namespace impl {
namespace cuts {
{%- for c in conditions -%}
{% include 'cuts/'~ c.objects[0].type ~'_cuts.hxx' %}
{% endfor -%}
} // namespace cuts
} // namespace impl

#endif
{% endblock code %}
