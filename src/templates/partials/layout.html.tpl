{% include "partials/doctype.html.tpl" %}
<head>
    {% block head %}
        {% include "partials/content_type.html.tpl" %}
        {% include "partials/includes.html.tpl" %}
        <title>Instashow</title>
    {% endblock %}
</head>
<body class="ux">
    <div id="overlay"></div>
    <div id="header">
        {% block header %}
            <h1>{% block name %}{% endblock %}</h1>
            <div class="links">
                {% if link == "home" %}
                    <a href="{{ url_for('index') }}" class="active">home</a>
                {% else %}
                    <a href="{{ url_for('index') }}">home</a>
                {% endif %}
                //
                {% if link == "customers" %}
                    <a href="{{ url_for('list_customers') }}" class="active">customers</a>
                {% else %}
                    <a href="{{ url_for('list_customers') }}">customers</a>
                {% endif %}
                //
                {% if link == "suppliers" %}
                    <a href="{{ url_for('list_suppliers') }}" class="active">suppliers</a>
                {% else %}
                    <a href="{{ url_for('list_suppliers') }}">suppliers</a>
                {% endif %}
                //
                {% if link == "about" %}
                    <a href="{{ url_for('about') }}" class="active">about</a>
                {% else %}
                    <a href="{{ url_for('about') }}">about</a>
                {% endif %}
            </div>
        {% endblock %}
    </div>
    <div id="content">{% block content %}{% endblock %}</div>
    {% include "partials/footer.html.tpl" %}
</body>
{% include "partials/end_doctype.html.tpl" %}
