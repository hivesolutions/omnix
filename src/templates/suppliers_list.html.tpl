{% extends "partials/layout.html.tpl" %}
{% block title %}Suppliers{% endblock %}
{% block name %}Suppliers{% endblock %}
{% block content %}
    <ul class="filter entities-list" data-infinite="true">
        <input type="text" class="text-field section-input filter-input" data-original_value="Search Suppliers" />
        <div class="data-source" data-url="{{ url_for('list_suppliers_json') }}" data-type="json" data-timeout="0"></div>
        <li class="template clear">
            <div class="name"><a href="#">%[name]</a></div>
            <div class="description">%[primary_contact_information.email]</div>
        </li>
        <div class="filter-no-results quote">
            No results found
        </div>
        <div class="filter-more">
            <span class="button">Load more</span>
        </div>
    </ul>
{% endblock %}
