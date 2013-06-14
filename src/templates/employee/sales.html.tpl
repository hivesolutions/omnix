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
                    <span class="value down">123454.34 €</span>
                </td>
                <td>
                    <span class="label">Sales Weight</span><br />
                    <span class="value down">2.23 %</span>
                </td>
                <td>
                    <span class="label">Commissions</span><br />
                    <span class="value up">1232.23 €</span>
                </td>
            </tr>
        </tbody>
    </table>
    <table class="table-list">
        <thead>
            <tr>
                <th class="left label" width="20%">Day</th>
                <th class="left label" width="30%">Sale</th>
                <th class="right label" width="25%">Total</th>
                <th class="right label" width="25%">Commission</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td class="left">Jan 29, 2013</td>
                <td class="left"><a href="#">DVD02323121</a></td>
                <td class="right">123.23 €</td>
                <td class="right">12.23 €</td>
            </tr>
            <tr>
                <td class="left">Jan 28, 2013</td>
                <td class="left"><a href="#">DVD02323121</a></td>
                <td class="right">123.23 €</td>
                <td class="right">12.23 €</td>
            </tr>
            <tr>
                <td class="left">Jan 27, 2013</td>
                <td class="left"><a href="#">DVD02323121</a></td>
                <td class="right">123.23 €</td>
                <td class="right">12.23 €</td>
            </tr>
            <tr>
                <td class="left">Jan 26, 2013</td>
                <td class="left"><a href="#">DVD02323121</a></td>
                <td class="right">123.23 €</td>
                <td class="right">12.23 €</td>
            </tr>
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
