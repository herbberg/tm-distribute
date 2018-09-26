{% extends "header.hxx" %}
{% block code %}
#ifndef impl_conditions_h
#define impl_conditions_h

#include "../impl/cuts.hxx"

namespace impl {
namespace conditions {

struct logic
{
    typedef ap_uint<1> signal_type;

    // Condition signals
{%- for condition in conditions %}
    signal_type {{ condition.name }};
{%- endfor %}

    /* Process input data and update condition signals. */
    void process(const in_data_t& in_data)
    {
#pragma HLS ARRAY_PARTITION variable=in_data.eg complete dim=1
#pragma HLS ARRAY_PARTITION variable=in_data.jet complete dim=1
#pragma HLS ARRAY_PARTITION variable=in_data.tau complete dim=1
#pragma HLS ARRAY_PARTITION variable=in_data.muon complete dim=1
{%- for c in conditions %}
{%- if c.objects[0].type in ('eg', 'jet', 'tau') %}
        {{ c.name }} = {{ c.type }}<{{ c.objects[0].type }}_obj_requ_t, {{ c.objects[0].type }}_obj_t ,{{ c.objects|count }}, 12>(cuts::{{ c.name }}, in_data.{{ c.objects[0].type }});
{%- elif c.objects[0].type == 'muon' %}
        {{ c.name }} = {{ c.type }}<{{ c.objects[0].type }}_obj_requ_t, {{ c.objects[0].type }}_obj_t ,{{ c.objects|count }}, 8>(cuts::{{ c.name }}, in_data.{{ c.objects[0].type }});
{%- endif %}
{%- endfor %}
    }
};

} // namespace conditions
} // namespace impl

#endif
{% endblock code %}
