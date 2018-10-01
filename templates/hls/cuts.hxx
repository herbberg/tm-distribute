{% extends "header.hxx" %}
{% block code %}
#ifndef impl_cuts_h
#define impl_cuts_h

namespace impl {
namespace cuts {
{% for c in conditions %}
{%- include 'cuts/%s_cuts.hxx' % c.objects[0].type -%}
{% endfor %}
} // namespace cuts
} // namespace impl

#endif
{% endblock code %}
