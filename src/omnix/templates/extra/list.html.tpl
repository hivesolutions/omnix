{% extends "partials/layout.html.tpl" %}
{% block title %}Extras{% endblock %}
{% block name %}Extras{% endblock %}
{% block content %}
    <ul>
        <li>
            <div class="name">
                <a href="{{ url_for('images_extras') }}">Images List</a>
            </div>
            <div class="description">Upload a list of images to be used in entities</div>
        </li>
        <li>
            <div class="name">
                <a href="{{ url_for('prices_extras') }}">Prices List</a>
            </div>
            <div class="description">Import list of prices to the current data source</div>
        </li>
        <li>
            <div class="name">
                <a href="{{ url_for('template_extras') }}">Template Applier</a>
            </div>
            <div class="description">Apply an image template to a base image</div>
        </li>
    </ul>
{% endblock %}
