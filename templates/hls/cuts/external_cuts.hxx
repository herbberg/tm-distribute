{% block code %}
const {{ c.objects[0].type }}_obj_requ_t {{ c.name }} = {
    .channel_id={{ c.objects[0].ext_channel_id }}
};
{% endblock code %}
