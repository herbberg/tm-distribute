{% block code %}
    {%- if c.charge_correlation %}
        {%- if c.objects|count == 2 %}
        {{ c.name }} = gtl::condition::muon_comb_double<gtl::cut::{{ c.objects[0].type }}, gtl::object::{{ c.objects[0].type }}, {{ c.objects|count }}, {{ c.objects[0].slice.minimum }}, {{ c.objects[0].slice.maximum }}>(cuts::{{ c.name }}, in_data[bx_{{c.objects[0].bx}}].{{ c.objects[0].type }}, charge_correlation[bx_{{c.objects[0].bx}}_{{c.objects[0].bx}}].cc_double);
        {%- elif c.objects|count == 3 %}
        {{ c.name }} = gtl::condition::muon_comb_triple<gtl::cut::{{ c.objects[0].type }}, gtl::object::{{ c.objects[0].type }}, {{ c.objects|count }}, {{ c.objects[0].slice.minimum }}, {{ c.objects[0].slice.maximum }}>(cuts::{{ c.name }}, in_data[bx_{{c.objects[0].bx}}].{{ c.objects[0].type }}, charge_correlation[bx_{{c.objects[0].bx}}_{{c.objects[0].bx}}].cc_triple);
        {%- elif c.objects|count == 4 %}
        {{ c.name }} = gtl::condition::muon_comb_quad<gtl::cut::{{ c.objects[0].type }}, gtl::object::{{ c.objects[0].type }}, {{ c.objects|count }}, {{ c.objects[0].slice.minimum }}, {{ c.objects[0].slice.maximum }}>(cuts::{{ c.name }}, in_data[bx_{{c.objects[0].bx}}].{{ c.objects[0].type }}, charge_correlation[bx_{{c.objects[0].bx}}_{{c.objects[0].bx}}].cc_quad);
        {%- endif %}
    {%- else %}
        {{ c.name }} = gtl::condition::{{ c.type }}<gtl::cut::{{ c.objects[0].type }}, gtl::object::{{ c.objects[0].type }}, {{ c.objects|count }}, {{ c.objects[0].slice.minimum }}, {{ c.objects[0].slice.maximum }}>(cuts::{{ c.name }}, in_data[bx_{{c.objects[0].bx}}].{{ c.objects[0].type }});
    {%- endif %}
{%- endblock code %}
