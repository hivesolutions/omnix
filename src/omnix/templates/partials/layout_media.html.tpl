{% extends "partials/layout.html.tpl" %}
{% block header %}
    {{ super() }}
    <div class="links sub-links">
        {% if sub_link == "info" %}
            <a href="{{ url_for('media_browser', id = media.object_id) }}" class="active">info</a>
        {% else %}
            <a href="{{ url_for('media_browser', id = media.object_id) }}">info</a>
        {% endif %}
        //
        {% if sub_link == "delete" %}
            <a href="{{ url_for('delete_media_browser', id = media.object_id) }}" class="active warning link-confirm"
               data-message="Do you really want to delete {{ media.object_id }}  ?">delete</a>
        {% else %}
            <a href="{{ url_for('delete_media_browser', id = media.object_id) }}" class="warning link-confirm"
               data-message="Do you really want to delete {{ media.object_id }} ?">delete</a>
        {% endif %}
    </div>
{% endblock %}
