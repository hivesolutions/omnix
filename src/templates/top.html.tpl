{% extends "partials/layout.html.tpl" %}
{% block title %}Top Sellers{% endblock %}
{% block name %}Top Sellers{% endblock %}
{% block content %}
    <div class="quote">{{ title }}</div>
    <div class="separator-horizontal"></div>
    <table class="table table-resume three">
        <tbody>
            <tr>
                {% for index in range(3) %}
                    <td>
                        <span class="label strong">{{ index + 1 }}º</span><br />
                        <a href="{{ session['omnix.base_url'] }}adm/employees/{{ top_employees[index].object_id }}">{{ top_employees[index].employee }}</a><br />
                        <span class="label">Dolce Vita Tejo</span><br />
                        <span class="label strong">{{ '%0.2f' % top_employees[index].amount_price_vat }} €</span>
                    </td>
                {% endfor %}
            </tr>
        </tbody>
    </table>
    <table class="table table-list">
        <thead>
            <tr>
                <th class="left label" width="6%">Rank</th>
                <th class="left label" width="30%">Seller</th>
                <th class="left label" width="30%">Store</th>
                <th class="right label" width="14%">Count</th>
                <th class="right label" width="20%">Sales</th>
            </tr>
        </thead>
        <tbody>
            {% for index in range(3, 10) %}
                <tr>
                    <td class="left">{{ index + 1 }}º</td>
                    <td class="left"><a href="{{ session['omnix.base_url'] }}adm/employees/{{ top_employees[index].object_id }}">{{ top_employees[index].employee }}</a></td>
                    <td class="left">Sede</td>
                    <td class="right">{{ '%d' % top_employees[index].number_sales }} x</td>
                    <td class="right">{{ '%0.2f' % top_employees[index].amount_price_vat }} €</td>
                </tr>
            {% endfor %}
        </tbody>
    </table>
    <table>
        <tbody>
            <tr>
                <td>
                    <div class="links">
                        <a href="{{ url_for('top', month = previous[0], year = previous[1]) }}">previous</a>
                        //
                        {% if has_next %}
                            <a href="{{ url_for('top', month = next[0], year = next[1]) }}">next</a>
                        {% else %}
                            <span>next</span>
                        {% endif %}
                    </div>
                </td>
            </tr>
        </tbody>
    </table>
{% endblock %}
