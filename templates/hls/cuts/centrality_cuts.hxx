{% block code %}
const gtl::cut::{{ c.objects[0].type }} {{ c.name }} = {
    .signal_id={{ c.objects[0].cent_channel_id }}
};
{% endblock code %}
