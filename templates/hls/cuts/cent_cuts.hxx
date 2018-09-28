{% block code %}
const {{ c.objects[0].type }}_signal_requ_t {{ c.name }} = {
    .signal_id={{ c.objects[0].cent_channel_id }}
};
{% endblock code %}
