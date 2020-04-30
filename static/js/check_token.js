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

function checkAuth(data){
    if (!data.success && data.invalid_token){
        window.location.replace(data.auth_link);
    }
}