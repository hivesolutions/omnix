{% extends "partials/layout.html.tpl" %}
{% block title %}Extras{% endblock %}
{% block name %}Extras{% endblock %}
{% block content %}
    <ul>
        <li>
            <div class="name">
                <a href="{{ url_for('prices_extras') }}">Price List</a>
            </div>
            <div class="description">Import list of prices to the current data source</div>
        </li>
    </ul>
{% endblock %}
