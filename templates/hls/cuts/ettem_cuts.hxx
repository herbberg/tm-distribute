{% block code %}
const gtl::cut::{{ c.objects[0].type }} {{ c.name }}[{{ c.objects|count }}] = {
{%- for o in c.objects %}
    {
        .pt={{ o.threshold|c_hex(4) }},
        .comparison_mode={{ o.comparison_mode }},
    },
{%- endfor %}
};
{% endblock code %}
