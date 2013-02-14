{% extends "partials/layout_store.html.tpl" %}
{% block title %}Stores{% endblock %}
{% block name %}Stores :: {{ store.object_id }}{% endblock %}
{% block content %}
    <div class="quote">{{ store.name }}</div>
    <div class="separator-horizontal"></div>
    <table class="table-resume">
        <tr>
            <td>
                <span class="label">Today's Sales</span><br />
                <span class="value down">{{ current.number_sales }}</span>
            </td>
            <td>
                <span class="label">Today's Amount</span><br />
                <span class="value up">{{ '%0.2f' % current.amount_price_vat }} €</span>
            </td>
        </tr>
    </table>
    <table border="0" class="table-list" cellpadding="0" cellspacing="0">
        <thead>
            <tr>
                <th class="left label" width="50%">Previous Days</th>
                <th class="right label" width="25%">Sales</th>
                <th class="right label" width="25%">Total</th>
            </tr>
        </thead>
        <tbody>
        	{% for day in days %}
	            <tr>
	                <td class="left">{{ day.date.strftime('%b %d, %Y') }}</td>
	                <td class="right">{{ day.number_sales }}</td>
	                <td class="right">{{ '%0.2f' % day.amount_price_vat }} €</td>
	            </tr>
            {% endfor %}
        </tbody>
    </table>    
{% endblock %}
