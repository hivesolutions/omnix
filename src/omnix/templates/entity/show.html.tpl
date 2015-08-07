{% extends "partials/layout_media.html.tpl" %}
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
            <tr>
                <td class="right label" width="50%">url</td>
                <td class="left value" width="50%">{{ media.url }}</td>
            </tr>
            <tr>
                <td class="right label" width="50%">visibility</td>
                <td class="left value" width="50%">{{ media.visibility }}</td>
            </tr>
            <tr>
                <td class="right label" width="50%">description</td>
                <td class="left value" width="50%">{{ media.description }}</td>
            </tr>
        </tbody>
    </table>
    <img class="media-image" src="{{ media.image_url }}" />
{% endblock %}
