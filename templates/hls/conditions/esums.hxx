{% block code %}
        {{ c.name }} = gtl::condition::esums(cuts::{{ c.name }}[0], in_data.{{ c.objects[0].type }}[0]);
{%- endblock code %}
