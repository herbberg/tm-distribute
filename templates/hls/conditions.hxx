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
#pragma HLS ARRAY_PARTITION variable=in_data.asymmetry_et complete dim=1
#pragma HLS ARRAY_PARTITION variable=in_data.asymmetry_ht complete dim=1
#pragma HLS ARRAY_PARTITION variable=in_data.asymmetry_ethf complete dim=1
#pragma HLS ARRAY_PARTITION variable=in_data.asymmetry_hthf complete dim=1
#pragma HLS ARRAY_PARTITION variable=in_data.mbt0hfp complete dim=1
#pragma HLS ARRAY_PARTITION variable=in_data.mbt0hfm complete dim=1
#pragma HLS ARRAY_PARTITION variable=in_data.mbt1hfp complete dim=1
#pragma HLS ARRAY_PARTITION variable=in_data.mbt1hfm complete dim=1
{% for c in conditions %}
        {%- include 'conditions/%s.hxx' % c.type -%}
{% endfor %}
    }
};

} // namespace conditions
} // namespace impl

#endif
{% endblock code %}
