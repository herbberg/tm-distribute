{% block code %}
        {{ c.name }} = gtl::condition::{{ c.type }}<{{ c.objects[0].type }}_obj_requ_t, {{ c.objects[0].type }}_obj_t, {{ c.objects|count }}, {{ c.objects[0].slice.minimum }}, {{ c.objects[0].slice.maximum }}>(cuts::{{ c.name }}, in_data.{{ c.objects[0].type }});
{%- endblock code %}
