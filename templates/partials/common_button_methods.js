
        $("#sm_home_page").click(function(){ window.location.href = "/"; });
        $("#sm_pictures_page").click(function(){ window.location.href = "/pictures"; });
        $("#sm_about_page").click(function(){ window.location.href = "/about"; });

        $("#lg_home_page").click(function(){ window.location.href = "/"; });
        $("#lg_pictures_page").click(function(){ window.location.href = "/pictures"; });
        $("#lg_about_page").click(function(){ window.location.href = "/about"; });

        {% if uis['camera'] == 'active' %}
                $("#sm_take_picture").click(function(){ take_picture(); });
                $("#lg_take_picture").click(function(){ take_picture(); });
        {% endif %}

        function take_picture() {
            $.get("/ajax/take_picture", function(data, status){
            return false;
        });
    }
