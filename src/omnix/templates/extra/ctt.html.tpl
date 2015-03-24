{% extends "partials/layout.html.tpl" %}
{% block title %}CTT Shipping{% endblock %}
{% block name %}CTT Shipping{% endblock %}
{% block content %}
    <div class="quote">
        The current operation will generate a file containing all the pending
        (to be shipped) orders using the CTT defined format. The resulting file
        will be encoded using the Windows-1252 encoding as defined in the standard.
        <strong>This operation may take some time</strong>, be patient.
    </div>
    <div class="separator-horizontal"></div>
    <div class="quote error">
        {{ error }}
    </div>
    <form action="{{ url_for('do_ctt_extras') }}" method="post" class="form small">
        <span class="button" data-link="{{ url_for('list_extras') }}">Cancel</span>
        //
        <span class="button" data-submit="true">Generate</span>
    </form>
{% endblock %}
