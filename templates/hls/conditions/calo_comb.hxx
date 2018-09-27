{% block code %}
{%- for c in conditions %}
{%- if c.objects[0].type in ('eg', 'jet', 'tau') %}
        {{ c.name }} = {{ c.type }}<{{ c.objects[0].type }}_obj_requ_t, {{ c.objects[0].type }}_obj_t ,{{ c.objects|count }}, 12>(cuts::{{ c.name }}, in_data.{{ c.objects[0].type }});
{% endif -%}
{% endfor -%}
{% endblock code %}
