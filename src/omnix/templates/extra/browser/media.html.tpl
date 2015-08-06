{% extends "partials/layout.html.tpl" %}
{% block title %}Media{% endblock %}
{% block name %}{{ media.object_id }}{% endblock %}
{% block content %}
    <div class="quote">{{ media.object_id }}</div>
    <div class="separator-horizontal"></div>
    <table>
        <tbody>
        	<tr>
                <td class="right label" width="50%">engine</td>
                <td class="left value" width="50%">{{ media.engine }}</td>
            </tr>
            <tr>
                <td class="right label" width="50%">position</td>
                <td class="left value" width="50%">{{ media.position }}</td>
            </tr>
            <tr>
                <td class="right label" width="50%">label</td>
                <td class="left value" width="50%">{{ media.label }}</td>
            </tr>
            <tr>
                <td class="right label" width="50%">dimensions</td>
                <td class="left value" width="50%">{{ media.dimensions }}</td>
            </tr>
            <tr>
                <td class="right label" width="50%">mime type</td>
                <td class="left value" width="50%">{{ media.mime_type }}</td>
            </tr>
        </tbody>
    </table>
    <img src="{{ media.image_url }}" />
{% endblock %}
