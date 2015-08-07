{% extends "partials/layout_entity.html.tpl" %}
{% block title %}Entity{% endblock %}
{% block name %}{{ entity.object_id }}{% endblock %}
{% block content %}
    <form action="{{ url_for('update_entities', id = entity.object_id) }}" method="post" class="form">
        <div class="label">
            <label>Description</label>
        </div>
        <div class="input">
            <input class="text-field" name="description" placeholder="eg: a simple description"
                   value="{{ entity.description|default('', True) }}" data-error="{{ errors.description }}" />
        </div>
        <span class="button" data-link="{{ url_for('show_entities', id = entity.object_id) }}">Cancel</span>
        //
        <span class="button" data-submit="true">Update</span>
    </form>
{% endblock %}
