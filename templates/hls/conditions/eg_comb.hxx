{% block code %}
<<<<<<< HEAD
        {{ c.name }} = {{ c.type }}<{{ c.objects[0].type }}_obj_requ_t, {{ c.objects[0].type }}_obj_t ,{{ c.objects|count }}, 12>(cuts::{{ c.name }}, in_data.{{ c.objects[0].type }});
{%- endblock code %}
=======
        {{ c.name }} = {{ c.type }}<{{ c.objects[0].type }}_obj_requ_t, {{ c.objects[0].type }}_obj_t , {{ c.objects|count }}, {{ c.objects[0].slice.maximum }}+1, {{ c.objects[0].slice.minimum }}, {{ c.objects[0].slice.maximum }}>(cuts::{{ c.name }}, in_data.{{ c.objects[0].type }});
{% endblock code %}
>>>>>>> upstream/master
