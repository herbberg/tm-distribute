{% block code %}
const gtl::cut::{{ c.objects[0].type }} {{ c.name }}[{{ c.objects|count }}] = {
{%- for o in c.objects %}
    {
        .count={{ o.threshold|c_hex(1) }},
        .comparison_mode={{ o.comparison_mode }},
    },
{%- endfor %}
};
{% endblock code %}
