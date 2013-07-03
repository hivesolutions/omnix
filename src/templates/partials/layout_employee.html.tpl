{% extends "partials/layout.html.tpl" %}
{% block header %}
    {{ super() }}
    <div class="links sub-links">
    	{% if is_self %}
	        {% if sub_link == "info" %}
	            <a href="{{ url_for('show_employee') }}" class="active">info</a>
	        {% else %}
	            <a href="{{ url_for('show_employee') }}">info</a>
	        {% endif %}
	        //
	        {% if sub_link == "sales" %}
	            <a href="{{ url_for('sales_employee') }}" class="active">sales</a>
	        {% else %}
	            <a href="{{ url_for('sales_employee') }}">sales</a>
	        {% endif %}
	    {% else %}
	        {% if sub_link == "info" %}
	            <a href="{{ url_for('show_employees', id = employee.object_id) }}" class="active">info</a>
	        {% else %}
	            <a href="{{ url_for('show_employees', id = employee.object_id) }}">info</a>
	        {% endif %}
	        //
	        {% if sub_link == "sales" %}
	            <a href="{{ url_for('sales_employees', id = employee.object_id) }}" class="active">sales</a>
	        {% else %}
	            <a href="{{ url_for('sales_employees', id = employee.object_id) }}">sales</a>
	        {% endif %}
	    {% endif %}
    </div>
{% endblock %}
