{% block code %}
const gtl::cut::signal {{ c.name }} = {
    .signal_id={{ c.objects[0].ext_channel_id }}
};
{% endblock code %}
