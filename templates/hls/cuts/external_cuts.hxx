{% block code %}
const {{ c.objects[0].type }}_obj_requ_t {{ c.name }}[{{ c.objects|count }}] = {
{%- for o in c.objects %}
    {
        // tbd
    },
{% endfor -%}
};
{% endblock code %}
