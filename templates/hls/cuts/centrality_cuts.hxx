{% block code %}
const gtl::cut::signal {{ c.name }} = {
    .signal_id={{ c.objects[0].cent_channel_id }}
};
{% endblock code %}
