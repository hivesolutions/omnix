{% extends "email/macros.html.tpl" %}
{% block html %}
    <!DOCTYPE html>
    <html lang="en">
    <head>
        {% block head %}
            <title>{% block title %}{% endblock %}</title>
            <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        {% endblock %}
    </head>
    <body style="font-family:Helvetica,Arial,sans-serif;font-size:14px;line-height:24px;color:#4d4d4d;text-align:left;padding:0px 0px 0px 0px;margin:0px 0px 0px 0px;" bgcolor="#edece4">
        <div class="container" style="background-color:#edece4;margin:0px auto 0px auto;padding:48px 0px 48px 0px;" bgcolor="#edece4">
            <div style="background-color:#ffffff;width:520px;margin:0px auto 0px auto;padding:42px 72px 42px 72px;border:1px solid #d9d9d9;">
                {% if settings.logo %}
                    <div class="logo" style="text-align:right;">
                        <img src="{{ base_url }}/static/images/email/logo.png" alt="logo" />
                    </div>
                {% endif %}
                <div class="content">
                    {{ h1(self.title()) }}
                    {% block content %}{% endblock %}
                </div>
                <div class="footer" style="font-size:10px;line-height:16px;text-align:right;margin-top: 48px;">
                    &copy; 2008-2025 Hive Solutions &middot; All rights reserved<br/>
                    You are receiving this email because you are an Omni member.
                </div>
            </div>
        </div>
    </body>
    </html>
{% endblock %}
