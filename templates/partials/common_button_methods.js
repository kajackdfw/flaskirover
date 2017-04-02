
        $("#sm_home_page").click(function(){ window.location.href = "/"; });
        $("#sm_pictures_page").click(function(){ window.location.href = "/pictures"; });
        $("#sm_settings_page").click(function(){ window.location.href = "/settings"; });

        $("#lg_home_page").click(function(){ window.location.href = "/"; });
        $("#lg_pictures_page").click(function(){ window.location.href = "/pictures"; });
        $("#lg_settings_page").click(function(){ window.location.href = "/settings"; });

        {% if uis['camera'] == 'active' %}
                $("#sm_take_picture").click(function(){ take_picture(); });
                $("#lg_take_picture").click(function(){ take_picture(); });
        {% endif %}

        function take_picture() {
            $.get("/ajax/take_picture", function(data, status){
            return false;
        });
    }
