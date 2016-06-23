{% extends "partials/layout_entity.html.tpl" %}
{% block title %}Entity{% endblock %}
{% block name %}{{ entity.object_id }}{% endblock %}
{% block content %}
    <div class="quote">{{ entity.object_id }}</div>
    <div class="separator-horizontal"></div>
    <table>
        <tbody>
            <tr>
                <td class="right label" width="50%">class</td>
                <td class="left value" width="50%">{{ entity._class }}</td>
            </tr>
            <tr>
                <td class="right label" width="50%">status</td>
                <td class="left value" width="50%">{{ entity.status }}</td>
            </tr>
            <tr>
                <td class="right label" width="50%">representation</td>
                <td class="left value" width="50%">{{ entity.representation|default("n/a", True) }}</td>
            </tr>
            <tr>
                <td class="right label" width="50%">description</td>
                <td class="left value" width="50%">{{ entity.description|default("n/a", True) }}</td>
            </tr>
            <tr>
                <td class="right label" width="50%">metadata</td>
                <td class="left value" width="50%">{{ entity.metadata_s|default('n/a', True) }}</td>
            </tr>
        </tbody>
    </table>
{% endblock %}
