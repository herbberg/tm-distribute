{% block code %}
{%- for c in conditions -%}
{%- if c.objects[0].type == 'tau' %}
const {{ c.objects[0].type }}_obj_requ_t {{ c.name }}[{{ c.objects|count }}] = {
{%- for o in c.objects %}
    {
        .n_cuts={{ c.objects|count }},
        .n_obj={{ o.slice.maximum }},
        .pt={{ o.threshold|c_hex(4) }},
        .eta={{ o.eta|c_init_list }},
        .n_eta={{ o.eta|count }},
        .phi={{ o.phi|c_init_list }},
        .n_phi={{ o.phi|count }},
        .iso_lut={{ o.isolationLUT }},
    },
{% endfor -%}
};
{% endif -%}
{% endfor -%}
{% endblock code %}
