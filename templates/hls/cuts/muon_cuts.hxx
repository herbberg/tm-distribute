{% block code %}
const gtl::cut::{{ c.objects[0].type }} {{ c.name }}[{{ c.objects|count }}] = {
{%- for o in c.objects %}
    {
        .slice={{ o.slice }},
        .pt={{ o.threshold|c_hex(4) }},
        .comparison_mode={{ o.comparison_mode }},
        .eta={{ o.eta|c_init_list }},
        .n_eta={{ o.eta|count }},
        .phi={{ o.phi|c_init_list }},
        .n_phi={{ o.phi|count }},
        .iso_lut={{ o.isolationLUT }},
        .qual_lut={{ o.qualityLUT }},
        .requested_charge=gtl::cut::{{ c.objects[0].type }}::{{ o.charge }},
        {% if c.charge_correlation %}.requested_charge_correlation=gtl::cut::muon::{{ c.charge_correlation }},{%- endif %}
    },
{%- endfor %}
};
{% endblock code %}
