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
{% for c in conditions %}
        {%- include 'conditions/comb_conditions.hxx' -%}
{% endfor %}
    }
};

} // namespace conditions
} // namespace impl

#endif
{% endblock code %}
