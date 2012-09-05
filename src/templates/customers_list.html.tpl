{% extends "partials/layout.html.tpl" %}
{% block title %}Customers{% endblock %}
{% block name %}Customers{% endblock %}
{% block content %}
    <ul>
        {% for customer in customers %}
            <li>
                <div class="name">
                    <a href="#">{{ customer.name }}</a>
                </div>
                <div class="description">
                    {{ customer.primary_contact_information.email|default('&nbsp;', true) }}
                </div>
            </li>
        {% endfor %}
    </ul>
{% endblock %}
