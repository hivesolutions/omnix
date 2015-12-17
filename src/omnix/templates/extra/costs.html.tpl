{% extends "partials/layout.html.tpl" %}
{% block title %}Cost List{% endblock %}
{% block name %}Cost List{% endblock %}
{% block content %}
    <div class="quote">
        Please provide the file containing the list of costs to be imported
        to the data source, the file should be <strong>excell and key value
        based</strong> associating the product id with its cost.<br />
        Remember this is a <strong>dangerous operation</strong>.
    </div>
    <div class="separator-horizontal"></div>
    <div class="quote error">
        {{ error }}
    </div>
    <form enctype="multipart/form-data" action="{{ url_for('do_costs_extras') }}" method="post" class="form small">
        <div class="input">
             <a data-name="costs_file" class="uploader">Select & Upload the cost list file</a>
        </div>
        <span class="button" data-link="{{ url_for('list_extras') }}">Cancel</span>
        //
        <span class="button" data-submit="true">Upload</span>
    </form>
{% endblock %}
