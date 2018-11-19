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
    void process(const in_data_t in_data[N_BX_DATA], const cc_bx_comb_t charge_correlation[cc_bx_comb_type::bx_comb_size])
    {
#pragma HLS ARRAY_PARTITION variable=in_data.eg complete dim=0
#pragma HLS ARRAY_PARTITION variable=in_data.jet complete dim=0
#pragma HLS ARRAY_PARTITION variable=in_data.tau complete dim=0
#pragma HLS ARRAY_PARTITION variable=in_data.muon complete dim=0
#pragma HLS ARRAY_PARTITION variable=in_data.ett complete dim=0
#pragma HLS ARRAY_PARTITION variable=in_data.htt complete dim=0
#pragma HLS ARRAY_PARTITION variable=in_data.etm complete dim=0
#pragma HLS ARRAY_PARTITION variable=in_data.htm complete dim=0
#pragma HLS ARRAY_PARTITION variable=in_data.ettem complete dim=0
#pragma HLS ARRAY_PARTITION variable=in_data.etmhf complete dim=0
#pragma HLS ARRAY_PARTITION variable=in_data.asymmetry_et complete dim=0
#pragma HLS ARRAY_PARTITION variable=in_data.asymmetry_ht complete dim=0
#pragma HLS ARRAY_PARTITION variable=in_data.asymmetry_ethf complete dim=0
#pragma HLS ARRAY_PARTITION variable=in_data.asymmetry_hthf complete dim=0
#pragma HLS ARRAY_PARTITION variable=in_data.mbt0hfp complete dim=0
#pragma HLS ARRAY_PARTITION variable=in_data.mbt0hfm complete dim=0
#pragma HLS ARRAY_PARTITION variable=in_data.mbt1hfp complete dim=0
#pragma HLS ARRAY_PARTITION variable=in_data.mbt1hfm complete dim=0
#pragma HLS ARRAY_PARTITION variable=charge_correlation.cc_double complete dim=0
#pragma HLS ARRAY_PARTITION variable=charge_correlation.cc_triple complete dim=0
#pragma HLS ARRAY_PARTITION variable=charge_correlation.cc_quad complete dim=0
        
        using namespace cc_bx_comb_type;
{% for c in conditions %}
        {%- include 'conditions/%s.hxx' % c.type -%}
{% endfor %}
    }
};

} // namespace conditions
} // namespace impl

#endif
{% endblock code %}
