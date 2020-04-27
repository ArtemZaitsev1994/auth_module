$(document).ready(function(){

    function showError(error){
        $('#error').html(error);
    }
    
    login = function(e){
        errors = ''

        if ($('#Password').val().length < 1) {
            errors += 'Укажите пароль.<br>'
        }
        if ($('#Login').val().length < 1) {
            errors += 'Укажите логин.<br>'
        }

        if (errors){
            showError(errors)
            return
        }

        searchParams = new URLSearchParams(window.location.search)
        service = searchParams.get('service')
        section = searchParams.get('section')

        q_data = {
            'login': $('#Login').val(),
            'password': $('#Password').val(),
            'service': service,
            'section': section
        }


        $.ajax({
            dataType: 'json',
            url: '/login',
            type: 'POST',
            data: JSON.stringify(q_data),
            success: function(data){
                console.log(data)
                if (data.success){
                    // localStorage.setItem(`${service}_auth`, `Bearer ${data.token}`)
                    // console.log(localStorage.getItem(`${service}_auth`))
                    window.location.href = data.auth_link;
                } else {
                    showError(data.message)
                }
            }
        });

    }

    $('#submit').click(login)
    $('input').on('keydown', function(e){
        if (e.keyCode == 13) {
            login()
        }
    })
});
