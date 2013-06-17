<div id="footer">
    {% block footer %}
        &copy; Copyright 2008-2012 by <a href="http://hive.pt">Hive Solutions</a>.<br />
        {% if session['omnix.username'] %}<a href="#">{{ session['omnix.username'] }}</a> // <a href="{{ url_for('logout') }}">logout</a><br />{% endif %}
    {% endblock %}
</div>
