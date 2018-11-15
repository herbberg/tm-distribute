{% block code %}
        {{ c.name }} = gtl::condition::{{ c.type }}<gtl::cut::{{ c.objects[0].type }}, gtl::object::{{ c.objects[0].type }}, {{ c.objects|count }}, {{ c.objects[0].slice.minimum }}, {{ c.objects[0].slice.maximum }}>(cuts::{{ c.name }}, in_data[bx_{{c.objects[0].bx}}].{{ c.objects[0].type }}{% if c.charge_correlation %}, in_data[bx_{{c.objects[0].bx}}].cc_double, in_data[bx_{{c.objects[0].bx}}].cc_triple, in_data[bx_{{c.objects[0].bx}}].cc_quad {%- endif %});
{%- endblock code %}
