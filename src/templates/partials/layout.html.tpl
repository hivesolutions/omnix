{% include "partials/doctype.html.tpl" %}
<head>
    {% block head %}
        {% include "partials/content_type.html.tpl" %}
        {% include "partials/includes.html.tpl" %}
        <title>Omnix</title>
    {% endblock %}
</head>
<body class="ux">
    <div id="overlay" class="overlay"></div>
    <div id="header">
        {% block header %}
            <h1>{% block name %}{% endblock %}</h1>
            <div class="links">
                {% if link == "home" %}
                    <a href="{{ url_for('index') }}" class="active">home</a>
                {% else %}
                    <a href="{{ url_for('index') }}">home</a>
                {% endif %}
                {% if acl("customers.customer_person.list") %}
                    //
                    {% if link == "customers" %}
                        <a href="{{ url_for('list_customers') }}" class="active">customers</a>
                    {% else %}
                        <a href="{{ url_for('list_customers') }}">customers</a>
                    {% endif %}
                {% endif %}
                {% if acl("foundation.supplier_company.list") %}
                    //
                    {% if link == "suppliers" %}
                        <a href="{{ url_for('list_suppliers') }}" class="active">suppliers</a>
                    {% else %}
                        <a href="{{ url_for('list_suppliers') }}">suppliers</a>
                    {% endif %}
                {% endif %}
                {% if acl("foundation.store.list") %}
                    //
                    {% if link == "stores" %}
                        <a href="{{ url_for('list_stores') }}" class="active">stores</a>
                    {% else %}
                        <a href="{{ url_for('list_stores') }}">stores</a>
                    {% endif %}
                {% endif %}
                //
                {% if link == "about" %}
                    <a href="{{ url_for('about') }}" class="active">about</a>
                {% else %}
                    <a href="{{ url_for('about') }}">about</a>
                {% endif %}
                //
                <div class="links-extra">
                    <ul>
                        <li>
                            {% if acl("foundation.employee.list") %}
                                {% if link == "employees" %}
                                    <a href="{{ url_for('list_employees') }}" class="active">employees</a>
                                {% else %}
                                    <a href="{{ url_for('list_employees') }}">employees</a>
                                {% endif %}
                            {% endif %}
                        </li>
                        <li>
                            {% if link == "reports" %}
                                <a href="{{ url_for('list_reports') }}" class="active">reports</a>
                            {% else %}
                                <a href="{{ url_for('list_reports') }}">reports</a>
                            {% endif %}
                        </li>
                        <li>
                            {% if link == "extras" %}
                                <a href="{{ url_for('list_extras') }}" class="active">extras</a>
                            {% else %}
                                <a href="{{ url_for('list_extras') }}">extras</a>
                            {% endif %}
                        </li>
                        <li>
                            {% if link == "top" %}
                                <a href="{{ url_for('top') }}" class="active">top sellers</a>
                            {% else %}
                                <a href="{{ url_for('top') }}">top sellers</a>
                            {% endif %}
                        </li>
                    </ul>
                </div>
                <a class="link link-more">
                    <span>more</span>
                </a>
            </div>
        {% endblock %}
    </div>
    <div id="content">{% block content %}{% endblock %}</div>
    {% include "partials/messages.html.tpl" %}
    {% include "partials/footer.html.tpl" %}
</body>
{% include "partials/end_doctype.html.tpl" %}
