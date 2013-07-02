{% extends "partials/layout_employee.html.tpl" %}
{% block title %}Employees{% endblock %}
{% block name %}{{ employee.short_name }}{% endblock %}
{% block content %}
    <div class="quote">January 2013</div>
    <div class="separator-horizontal"></div>
    <table class="table-resume three">
        <tbody>
            <tr>
                <td>
                    <span class="label">Sales Amount</span><br />
                    <span class="value">{{ "%.2f" % sales_total }} €</span>
                </td>
                <td>
                    <span class="label">Sales Count</span><br />
                    <span class="value">{{ sales_count }}</span>
                </td>
                <td>
                    <span class="label">Commissions</span><br />
                    <span class="value">{{ "%.2f" % (sales_total * 0.02) }} €</span>
                </td>
            </tr>
        </tbody>
    </table>
    <table class="table-list">
        <thead>
            <tr>
                <th class="left label" width="20%">Day</th>
                <th class="left label" width="30%">Sale</th>
                <th class="right label" width="25%">Value</th>
                <th class="right label" width="25%">Commission</th>
            </tr>
        </thead>
        <tbody>
            {% for sale in sales %}
                <tr>
                    <td class="left">Jan 29, 2013</td>
                    <td class="left"><a href="#">{{ sale.identifier }}</a></td>
                    <td class="right">{{ "%.2f" % sale.price_vat }} €</td>
                    <td class="right">{{ "%.2f" % (sale.price_vat * 0.02) }} €</td>
                </tr>
            {% endfor %}
        </tbody>
    </table>
    <table>
        <tbody>
            <tr>
                <td>
                    <div class="links">
                        <a href="#">previous</a> // <a href="#">next</a>
                    </div>
                </td>
            </tr>
        </tbody>
    </table>
{% endblock %}
