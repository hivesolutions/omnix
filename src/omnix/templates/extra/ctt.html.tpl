{% extends "partials/layout.html.tpl" %}
{% block title %}CTT Shipping{% endblock %}
{% block name %}CTT Shipping{% endblock %}
{% block content %}
    <div class="quote">
        Please provide the file containing the list of prices to be imported
        to the data source, the file should be <strong>excell and key value
        based</strong> associating the product id with its price.<br />
        Remember this is a <strong>dangerous operation</strong>.
    </div>
    <div class="separator-horizontal"></div>
    <div class="quote error">
        {{ error }}
    </div>
    <form action="{{ url_for('do_ctt_extras') }}" method="post" class="form no-async small">
        <span class="button" data-link="{{ url_for('list_extras') }}">Cancel</span>
        //
        <span class="button" data-submit="true">Generate</span>
    </form>
{% endblock %}
