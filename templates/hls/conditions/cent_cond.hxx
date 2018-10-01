{% block code %}
        {{ c.name }} = {{ c.type }}(cuts::{{ c.name }}, in_data.{{ c.objects[0].type }});
{%- endblock code %}
