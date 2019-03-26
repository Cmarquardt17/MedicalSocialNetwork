/*global WildRydes _config*/

var WildRydes = window.WildRydes || {};

(function rideScopeWrapper($) {
    var authToken;
    WildRydes.authToken.then(function setAuthToken(token) {
        if (token) {
            authToken = token;
        } else {
            window.location.href = '/login.html';
        }
    }).catch(function handleTokenError(error) {
        alert(error);
        window.location.href = '/login.html';
    });
    function saveInfo(FirstName) {
        $.ajax({
            method: 'POST',
            url: _config.api.invokeUrl + '/userInfo',
            headers: {
                Authorization: authToken
            },
            data: JSON.stringify({
                FirstName: firstName
            }),
            contentType: 'application/json',
            success: completeInfo,
            error: function ajaxError(jqXHR, textStatus, errorThrown) {
                console.error('Error requesting ride: ', textStatus, ', Details: ', errorThrown);
                console.error('Response: ', jqXHR.responseText);
                alert('An error occured when requesting your information:\n' + jqXHR.responseText);
            }
        });
    }


 function completeInfo(result) {
      console.log('We got to completeInfo');
        var name;
        var pronoun;
        console.log('Response received from API: ', result);

    }

    function handleRequestClick(event) {
        var FirstName = "Cole";
        var pickupLocation = WildRydes.selectedPoint = {
                latitude: -111.04,
                longitude: 45.67
            };
        event.preventDefault();
        completeInfo(pickupLocation);
    }

    function displayUpdate(text) {
        $('#updates').append($('<li>' + text + '</li>'));
    }
}(jQuery));
