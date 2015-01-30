{% extends "partials/layout.html.tpl" %}
{% block title %}Template Applier{% endblock %}
{% block name %}Template Applier{% endblock %}
{% block content %}
    <div class="quote">
        Please provide the file containing the base image to be used in the
        generation of a final image from a mask. Use the <strong>best quality
        possible</strong> to avoid unwanted results.
    </div>
    <div class="separator-horizontal"></div>
    <div class="quote error">
        {{ error }}
    </div>
    {% if acl("foundation.system_company.show.self") %}
        <form enctype="multipart/form-data" action="{{ url_for('do_template_extras') }}" method="post" class="form no-async small">
            <div class="input">
                 <a data-name="base_file" class="uploader">Select & Upload the base image</a>
            </div>
            <span class="button" data-link="{{ url_for('list_extras') }}">Cancel</span>
            //
            <span class="button" data-submit="true">Convert</span>
        </form>
    {% endif %}
    <div class="quote">
        Provide the file containing the template image that is going to be
        applied to the base image to generate the final image. Use the
        <strong>best quality possible</strong> to avoid unwanted results.
    </div>
    <div class="separator-horizontal"></div>
    {% if acl("foundation.root_entity.set_media") %}
        <form enctype="multipart/form-data" action="{{ url_for('do_mask_extras') }}" method="post" class="form small">
            <div class="input">
                 <a data-name="mask_file" class="uploader">Select & Upload the template image</a>
            </div>
            <span class="button" data-link="{{ url_for('list_extras') }}">Cancel</span>
            //
            <span class="button" data-submit="true">Upload</span>
        </form>
    {% endif %}
{% endblock %}
