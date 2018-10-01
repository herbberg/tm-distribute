{% block code %}
const gtl::cut::{{ c.objects[0].type }} {{ c.name }}[{{ c.objects|count }}] = {
{%- for o in c.objects %}
    {
        .n_cuts={{ c.objects|count }},
        .slice={{ o.slice }},
        .pt={{ o.threshold|c_hex(4) }},
        .comparison_mode={{ o.comparison_mode }},
        .eta={{ o.eta|c_init_list }},
        .n_eta={{ o.eta|count }},
        .phi={{ o.phi|c_init_list }},
        .n_phi={{ o.phi|count }},
    },
{%- endfor %}
};
{% endblock code %}
