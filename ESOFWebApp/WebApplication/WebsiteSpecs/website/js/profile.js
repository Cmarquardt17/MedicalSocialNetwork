/*global MSN _config*/

var Profiles = window.MSN || {};

(function rideScopeWrapper($) {
    var authToken;
    Profiles.authToken.then(function setAuthToken(token) {
        if (token) {
            authToken = token;
        } else {
            window.location.href = '/login.html';
        }
    }).catch(function handleTokenError(error) {
        alert(error);
        window.location.href = '/login.html';
    });

    function requestDoctor(pickupLocation) {
        $.ajax({
            method: 'POST',
            url: _config.api.invokeUrl + '/doctor',
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
                console.error('Error requesting ride: ', textStatus, ', Details: ', errorThrown);
                console.error('Response: ', jqXHR.responseText);
                alert('An error occured when requesting your doctor:\n' + jqXHR.responseText);
            }
        });
    }

	$(function profileFill(){
	var pickupLocation = Profiles.selectedPoint = {
                latitude: -111.04,
                longitude: 45.67
            };
        requestUserName(pickupLocation);
	});

	function requestUserName(pickupLocation) {
		$.ajax({
            method: 'POST',
            url: _config.api.invokeUrl + '/user',
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
            success: fillProfile,
            error: function ajaxError(jqXHR, textStatus, errorThrown) {
                console.error('Error requesting ride: ', textStatus, ', Details: ', errorThrown);
                console.error('Response: ', jqXHR.responseText);
                alert('An error occured when requesting a user:\n' + jqXHR.responseText);
            }
        });
	}

	function fillProfile(result) {
        var user;
        console.log('Response received from API: ', result);
        user = result.User;
		$('#name').text(user);
    }

    function completeRequest(result) {
        var doctor;
        var pronoun;
        console.log('Response received from API: ', result);
        doctor = result.Doctor;
        pronoun = doctor.Gender === 'Male' ? 'his' : 'her';
        displayUpdate('You are now friends with ' + doctor.Name);
    }

    // Register click handler for #request button
    $(function onDocReady() {

    	$('#request').text('Request Doctor');
    	$('#request').prop('disabled', false);
        $('#request').click(handleRequestClick);
        $('#signOut').click(function() {
            Profiles.signOut();
            alert("You have been signed out.");
            window.location = "login.html";
        });

        Profiles.authToken.then(function updateAuthMessage(token) {
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
        var pickupLocation = Profiles.selectedPoint = {
                latitude: -111.04,
                longitude: 45.67
            };
        event.preventDefault();
        requestDoctor(pickupLocation);
    }

    function displayUpdate(text) {
        $('#updates').append($('<li>' + text + '</li>'));
    }
}(jQuery));
