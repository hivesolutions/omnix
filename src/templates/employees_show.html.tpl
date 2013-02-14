{% extends "partials/layout.html.tpl" %}
{% block title %}Employees{% endblock %}
{% block name %}Employees :: {{ employee.object_id }}{% endblock %}
{% block content %}
    <div class="quote">{{ employee.representation }}</div>
    <div class="separator-horizontal"></div>
    <table>
        <tbody>
            <tr>
                <td class="right label" width="50%">phone</td>
                <td class="left value" width="50%">{{ employee.primary_contact_information.phone_number | default('', true) }}</td>
            </tr>
            <tr>
                <td class="right label" width="50%">email</td>
                <td class="left value" width="50%">{{ employee.primary_contact_information.email | default('', true) }}</td>
            </tr>
        </tbody>
    </table>
{% endblock %}
