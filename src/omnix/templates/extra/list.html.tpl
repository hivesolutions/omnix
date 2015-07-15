{% extends "partials/layout.html.tpl" %}
{% block title %}Extras{% endblock %}
{% block name %}Extras{% endblock %}
{% block content %}
    <ul>
        {% if acl("inventory.transactional_merchandise.update") %}
            <li>
                <div class="name">
                    <a href="{{ url_for('images_extras') }}">Images List</a>
                </div>
                <div class="description">Upload a list of images to be used in inventory</div>
            </li>
        {% endif %}
        {% if acl("inventory.transactional_merchandise.update") %}
            <li>
                <div class="name">
                    <a href="{{ url_for('prices_extras') }}">Prices List</a>
                </div>
                <div class="description">Import list of prices to the current data source</div>
            </li>
        {% endif %}
        {% if acl("sales.sale_order.list") %}
            <li>
                <div class="name">
                    <a href="{{ url_for('ctt_extras') }}">CTT Shipping</a>
                </div>
                <div class="description">Generate the standard shipping file for open sale orders</div>
            </li>
        {% endif %}
        {% if acl("foundation.system_company.show.self") %}
            <li>
                <div class="name">
                    <a href="{{ url_for('template_extras') }}">Template Applier</a>
                </div>
                <div class="description">Apply an image template to a base image</div>
            </li>
        {% endif %}
    </ul>
{% endblock %}
