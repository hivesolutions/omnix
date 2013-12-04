{% extends "partials/layout.html.tpl" %}
{% block title %}Images List{% endblock %}
{% block name %}Images List{% endblock %}
{% block content %}
    <div class="quote">
        Please provide the file containing the list of images to be imported
        to the data source, the file should be <strong>zip file
        based</strong> conatining image files with their names.<br />
        Remember this is a <strong>dangerous operation</strong>.
    </div>
    <div class="separator-horizontal"></div>
    <div class="quote error">
        {{ error }}
    </div>
    <form enctype="multipart/form-data" action="{{ url_for('do_images_extras') }}" method="post" class="form small">
        <div class="input">
             <a data-name="images_file" class="uploader">Select & Upload the images list file</a>
        </div>
        <span class="button" data-link="{{ url_for('list_extras') }}">Cancel</span>
        //
        <span class="button" data-submit="true">Upload</span>
    </form>
{% endblock %}