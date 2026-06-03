
{{ variable }}
{{ student.name}}
{{ student|length }}
{{ name|upper}}
{{ name|lower}}

{% for item in list %}
    {{ item }}
{% endfor %}

{% if condition %}
    Condition is true
{% elif other_condition %}
    Other condition is true
{% else %}
    Condition is false
{% endif %}

# to generate URL

{{url_for('function_name')}}

{% extends 'base.html' %}

{@block content %}

{% endblock %}

