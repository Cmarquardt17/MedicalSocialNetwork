/*global WildRydes _config*/

var WildRydes = window.WildRydes || {};

(function rideScopeWrapper($) {
    var authToken;
    WildRydes.authToken.then(function setAuthToken(token) {
        if (token) {
            authToken = token;
        } else {
            window.location.href = '/profile.html';
        }
    }).catch(function handleTokenError(error) {
        alert(error);
        window.location.href = '/profile.html';
    });
    function requestInfo(pickupLocation) {
    console.log('We got to requestInfo');
        $.ajax({
            method: 'POST',
            url: _config.api.invokeUrl + '/addinfo',
            headers: {
                Authorization: authToken
            }, 
            data: JSON.stringify({
                PickupLocation: {
                    Latitude: pickupLocation.latitude,
                    Longitude: pickupLocation.longitude
                }
            }),
            contentType: 'application/json',
            success: completeRequest,
            error: function ajaxError(jqXHR, textStatus, errorThrown) {
                console.error('Error requesting information: ', textStatus, ', Details: ', errorThrown);
                console.error('Response: ', jqXHR.responseText);
                alert('An error occured when requesting your info:\n' + jqXHR.responseText);
            }
        });
    }

    function completeRequest(result) {
      console.log('We got to completeRequest');
        var firstName;
        console.log('Response received from API: ', result);
        firstName = result.fName;
        displayUpdate('This is your name' + firstName.fName);
    }

    // Register click handler for #request button
    $(function onDocReady() {
      console.log('We got to onDocReady');
    	$('#submit').text('Request Doc');
    	$('#submit').prop('disabled', false);
        $('#submit').click(handleRequestClick);

        WildRydes.authToken.then(function updateAuthMessage(token) {
            if (token) {
                displayUpdate('You are authenticated. Click to see your <a href="#authTokenModal" data-toggle="modal">auth token</a>.');
                $('.authToken').text(token);
            }
        });

        if (!_config.api.invokeUrl) {
            $('#noApiMessage').show();
        }
    });

    function handleRequestClick(event) {
    console.log('We are at handleRequestClick');
        var pickupLocation = WildRydes.selectedPoint = {
                latitude: -111.04,
                longitude: 45.67
            };
        event.preventDefault();
        requestInfo(pickupLocation);
    }

    function displayUpdate(text) {
        $('#updates').append($('<li>' + text + '</li>'));
    }
}(jQuery));