{% extends "header.hxx" %}
{% block code %}
#ifndef impl_seeds_h
#define impl_seeds_h

#include "../impl/conditions.hxx"

#include <ap_int.h>

namespace impl {
namespace seeds {

struct logic
{
    typedef ap_uint<1> signal_type;
    typedef ::impl::conditions::logic conditions_logic_type;

    // Seed signals
  {%- for seed in seeds %}
    signal_type {{ seed.name }};
{%- endfor %}

    /* Process condition logic and update seed signals. */
    void process(const conditions_logic_type& {{ condition_namespace }})
    {
{%- for seed in seeds %}
        {{ seed.name }} = {{ seed.expression }};
{%- endfor %}
    }

    /* Map seed signals to output vector. */
    void map(signal_type seeds[N_ALGORITHMS])
    {
#pragma HLS ARRAY_PARTITION variable=seeds complete dim=1
{%- for seed in seeds %}
        seeds[{{ seed.index }}] = {{ seed.name }};
{%- endfor %}
    }

}; // struct logic

} // namespace seeds
} // namespace impl

#endif
{% endblock code %}
