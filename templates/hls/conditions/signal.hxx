{% block code %}
        {{ c.name }} = gtl::condition::{{ c.type }}(cuts::{{ c.name }}, in_data[bx_{{c.objects[0].bx}}].{{ c.objects[0].type }});
{%- endblock code %}
