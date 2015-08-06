{% extends "partials/layout.html.tpl" %}
{% block title %}New Media{% endblock %}
{% block name %}New Media{% endblock %}
{% block content %}
    <form enctype="multipart/form-data" action="{{ url_for('create_media_browser', id = object_id) }}"
    	  method="post" class="form">
        <div class="label">
		    <label>Position</label>
		</div>
        <div class="input">
            <input class="text-field" name="position" placeholder="eg: 1, 2, 3, etc." value="{{ media.position }}"
                   data-error="{{ errors.position }}" />
        </div>
        <div class="label">
		    <label>Label</label>
		</div>
        <div class="input">
            <input class="text-field" name="label" placeholder="eg: main_header" value="{{ media.label }}"
                   data-error="{{ errors.label }}" />
        </div>
        <div class="label">
		    <label>Description</label>
		</div>
        <div class="input">
            <textarea class="text-area" name="description" placeholder="eg: some words about the media"
                      data-error="{{ errors.description }}">{{ media.description }}</textarea>
        </div>
        <div class="input">
             <a data-name="media_file" class="uploader">Select & Upload the media list file</a>
        </div>
        <span class="button" data-link="{{ url_for('list_extras') }}">Cancel</span>
        //
        <span class="button" data-submit="true">Upload</span>
    </form>
{% endblock %}
