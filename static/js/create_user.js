$(document).ready(function(){
    local_token = localStorage.getItem('Authorization')
    cookie_token = $.cookie('Authorization')

    if (cookie_token === undefined && local_token === null){
        window.location.replace('/');
    } else if (cookie_token !== undefined){
        // если токен пришел в куках 
        // приходит, если мы залогинились только что -> валидный по определению
        localStorage.setItem('Authorization', cookie_token)
        $.removeCookie('Authorization', { path: '/' })
    } else if (local_token !== null){
        // если токен есть у нас в локал сторедже, проверям валидный ли он до сих пор
        $.ajax({
            dataType: 'json',
            url: '/api/check_token',
            type: 'POST',
            data: JSON.stringify({'token': local_token}),
            processData: false,
            contentType: false,
            beforeSend: function(request) {
                request.setRequestHeader("Authorization", local_token);
            },
            success: function(data){
                checkAuth(data)
            }
        })
    }
    token = localStorage.getItem('Authorization')

    function checkAuth(data){
        if (!data.success && data.invalid_token){
            window.location.replace(data.auth_link);
        }
    }

    function showError(error){
        $('#error').html(error);
    }

    function showSuccess(success){
        $('#success').html(success);
    }
    
    login = function(e){
        errors = ''

        if ($('#Password').val().length < 1) {
            errors += 'Укажите пароль.<br>'
        }
        if ($('#Login').val().length < 1 && $('#Email').val().length < 1) {
            errors += 'Укажите логин или e-mail.<br>'
        }

        services = []
        for (serv of $('.services')) {
            if (serv.checked) { services.push(serv.id) }
        }

        if (services.length == 0){
            errors += 'Выберите хотя бы один сервис.<br>'
        }

        if (errors){
            showError(errors)
            return
        }

        q_data = {
            'name': $('#Name').val(),
            'email': $('#Email').val(),
            'login': $('#Login').val(),
            'sername': $('#Sername').val(),
            'password': $('#Password').val(),
            'services': services,
        }

        $.ajax({
            dataType: 'json',
            url: '/api/create_user',
            type: 'POST',
            data: JSON.stringify(q_data),
            beforeSend: function(request) {
                request.setRequestHeader("Authorization", token);
            },
            success: function(data){
                checkAuth(data)
                if (data.success){
                    showSuccess(`Пользователь ${q_data.name} был добавлен`)
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
