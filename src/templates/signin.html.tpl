{% extends "partials/layout_simple.html.tpl" %}
{% block title %}Login{% endblock %}
{% block name %}Welcome To Omnix{% endblock %}
{% block content %}
    <div class="button login" data-link="{{ url_for('do_login') }}"></div>
{% endblock %}
