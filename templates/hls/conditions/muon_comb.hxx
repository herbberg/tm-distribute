{% block code %}
        {{ c.name }} = {{ c.type }}<{{ c.objects[0].type }}_obj_requ_t, {{ c.objects[0].type }}_obj_t ,{{ c.objects|count }}, 8>(cuts::{{ c.name }}, in_data.{{ c.objects[0].type }});
{% endblock code %}
