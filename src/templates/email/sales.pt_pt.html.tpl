{% extends "email/layout.pt_pt.html.tpl" %}
{% block title %}Relatório de Vendas{% endblock %}
{% block content %}
    <p>
        Este email confirma a sua reserva em {{ link(url_for("provider.show", name = schedule.provider.name), schedule.provider.full_name) }}
        com o numero de reserva {{ link(url_for("account.schedule_own", id = schedule.id), schedule.uuid_s()) }}. Esperáms que goste do serviço
        prestado pela mesma reserva.
    </p>
    {{ h2("Vendas & Deveoluções") }}
    <p>
        <table cellspacing="0" width="100%">
            <tr>
                <td width="100">
                    <strong>No.</strong>
                </td>
                <td>{{ schedule.uuid_s() }}</td>
            </tr>
            <tr>
                <td>
                    <strong>Nome</strong>
                </td>
                <td>{{ schedule.account.full_name() }} ({{ schedule.account.phone }})</td>
            </tr>
            <tr>
                <td>
                    <strong>Data</strong>
                </td>
                <td>{{ schedule.start_s() }}</td>
            </tr>
            <tr>
                <td>
                    <strong>Endereço</strong>
                </td>
                <td>{{ schedule.account.street }}</td>
            </tr>
            <tr>
                <td></td>
                <td>{{ schedule.account.zip_code }} {{ schedule.account.province }}</td>
            </tr>
            <tr>
                <td></td>
                <td>{{ schedule.account.country }}</td>
            </tr>
        </table>
    </p>
    {{ h2("Estamos Sempre Consigo") }}
    <p>
        Algum problema? A nossa equipa de apoio está disponível para o ajudar.
        Envie-nos um email para {{ link("mailto:ajuda@lugardajoia.com", "ajuda@lugardajoia.com", False) }}.
    </p>
{% endblock %}
