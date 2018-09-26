{% extends "header.hxx" %}
{% block code %}
#ifndef impl_cuts_h
#define impl_cuts_h

namespace impl {
namespace cuts {
{% include 'cuts/eg_cuts.hxx' %}
{% include 'cuts/jet_cuts.hxx' %}
{% include 'cuts/tau_cuts.hxx' %}
{% include 'cuts/muon_cuts.hxx' %}
} // namespace cuts
} // namespace impl

#endif
{% endblock code %}
