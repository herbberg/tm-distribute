{% block code %}
const gtl::cut::{{ c.objects[0].type }} {{ c.name }} = {
    .channel_id={{ c.objects[0].ext_channel_id }}
};
{% endblock code %}
