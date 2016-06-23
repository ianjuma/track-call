(navigator.geolocation.getCurrentPosition(function(position) {
  var phoneNumber = $('#phoneNumber').text();
  var cord = position.coords.latitude + ' ++ ' + position.coords.longitude;
  var data = { 'location': cord, 'url': document.URL, 'phoneNumber': phoneNumber };

  $.ajax({
    type: 'POST',
    url: '/api/location',
    data: data,
    dataType: 'application/json'
  });
}))();
