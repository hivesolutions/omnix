{% include "partials/doctype.html.tpl" %}
<head>
    {% block head %}
        {% include "partials/content_type.html.tpl" %}
        {% include "partials/includes.html.tpl" %}
        <title>Omnix</title>
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
                {% if link == "stores" %}
                    <a href="{{ url_for('list_stores') }}" class="active">stores</a>
                {% else %}
                    <a href="{{ url_for('list_stores') }}">stores</a>
                {% endif %}
                //
                {% if link == "employees" %}
                    <a href="{{ url_for('list_employees') }}" class="active">employees</a>
                {% else %}
                    <a href="{{ url_for('list_employees') }}">employees</a>
                {% endif %}
                //
                {% if link == "top" %}
                    <a href="{{ url_for('top') }}" class="active">top</a>
                {% else %}
                    <a href="{{ url_for('top') }}">top</a>
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
