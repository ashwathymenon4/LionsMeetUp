function login() {
  var cog_uri = "https://lionsmeetup.auth.us-east-1.amazoncognito.com/login?" + 
  "client_id=24ci6213vcpi0un21k2b51fh1d&response_type=token&scope=openid+phone+profile+email&redirect_uri="
  // console.log(cog_uri + redirect_uri)
  redirect_uri = location.protocol + '//' + location.host + "/callback.html"
  // console.log(redirect_uri)
  window.location.href = cog_uri + redirect_uri
}

function save_user_data() {
  const queryString = window.location.search;
  console.log(queryString);
}

function view_event(id) {
  // var doc_cookie = document.cookie;
  window.location.href = "/event.html?event_id=" + id // + "&user_id=" + 
}

function create_event() {
  var doc_cookie = document.cookie;
  if (!doc_cookie) {
    login();
  } else {
    cookie_pair = doc_cookie.split("=");
    cookie_json = JSON.parse(cookie_pair[1]);
    var uidd = cookie_json["user_data"]["user_id"]
    var place = autocomplete.getPlace()
    if(!place.geometry) {
      alert("Enter a valid place");
      return;
    }
    var lat = place.geometry.location.lat()
    var lng = place.geometry.location.lng()
    // var add_comps = place.address_components
    data = {
      "start_local": document.getElementById("start_time").value + ":00",
      "organizer_id": uidd,
      "name_text": document.getElementById("name").value,
      "end_local": document.getElementById("end_time").value + ":00",
      "description_text": document.getElementById("description").value,
      "category": $('#category').val(),
      "online_event": document.getElementById("online_event").checked,
      "longitude": lng,
      "latitude": lat,
      "address": document.getElementById("location").value,
      // "city": add_comps[add_comps.length - 3]["short_name"],
      // "postal_code": add_comps[add_comps.length - 1]["long_name"],
      // "region": add_comps[add_comps.length - 2]["short_name"],
    }
    // console.log(data)
    fetch('https://1ptsftnwde.execute-api.us-east-1.amazonaws.com/test/create-events', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(data => {
      window.location.href = "/event.html?event_id=" + data["body"]["item_id"]
      console.log(data);
    })
    .catch((error) => {
      // window.location.href = "/event_failure.html"
      console.log(error);
    });
  }
}

function update_profile(user_data) {
  json_data = {
    "email": user_data,
    "first_name": document.getElementById("first_name").value,
    "last_name": document.getElementById("last_name").value,
    "mobile": document.getElementById("mobile").value,
    "email": document.getElementById("email").value,
    "city": document.getElementById("city").value,
    "state": document.getElementById("state").value,
    "age": document.getElementById("age").value,
    "zip_code": document.getElementById("zip_code").value,
    "categories": $('#categories').val(),
    "gender": document.getElementById("gender").value,
    "address": document.getElementById("address").value
  }
  console.log(json_data)
  fetch('https://1ptsftnwde.execute-api.us-east-1.amazonaws.com/test/create-users', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify(json_data),
  })
  .then(response => response.json())
  .then(data => {
    console.log('Success:', data);
    alert("Updated!!");
    // window.location.href = "/profile.html?user_id=" + user_data
  })
  .catch((error) => {
    console.error('Error:', error);
    alert("Error Updating profile!! Please try again")
  });
}

function logout() {
  document.cookie = 'lions_data' + '=; expires=Thu, 01-Jan-70 00:00:01 GMT;';
  window.location.href = "/"
}

function join_event(event_id) {
  var c_json = check_cookie()
  new_event_id = event_id.split(".")[0]
  var user_id = c_json["user_data"]["user_id"];
  fetch("https://1ptsftnwde.execute-api.us-east-1.amazonaws.com/test/join-event?event_id=" + new_event_id + "&user_id=" + user_id, {
    method: 'GET'
  }).then(response => response.json())
  .then(data => {
    console.log(data)
    alert("Joined!!");
    var div = `
      <li class="d-flex justify-content-between align-items-start">
        <div class="ms-2 me-auto">
          <div class="fw-bold"><a href='/profile.html?id=`+ user_id + `'>`+ c_json["user_data"]["first_name"] +`</a></div>
        </div>
        <!-- <span class="badge bg-primary rounded-pill">14</span> -->
      </li>
    `
    document.getElementById("event_members").innerHTML += div;
  });
}

function check_cookie() {
  var doc_cookie = document.cookie;
  if(!doc_cookie) {
    alert("Please Login!!"); // need to change , models etc.,
    login();
  }
  cookie_pair = doc_cookie.split("=");
  cookie_json = JSON.parse(cookie_pair[1]);
  return cookie_json
}

function get_geo() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(position => {
      var lat = (position.coords.latitude).toString()
      var long = (position.coords.longitude).toString()
      fetch("https://1ptsftnwde.execute-api.us-east-1.amazonaws.com/test/geo-location?lat=" + lat + "&long=" + long, {
        method: 'GET'
      }).then(response => response.json())
      .then(data => {
        console.log(data);
        var location_data = JSON.parse(data["body"]);
        document.getElementById("city").value = location_data["city"];
        document.getElementById("state").value = location_data["state"];
        document.getElementById("zip_code").value = location_data["postcode"];
        document.getElementById("city").disabled = true;
        document.getElementById("state").disabled = true;
        document.getElementById("zip_code").disabled = true;
        var not_address_fields = ["city", "state", "zipcode", "postcode", "country", "country_code", "county","neighbourhood"]
        document.getElementById("address").value = ""
        for(key in location_data) {
          if(not_address_fields.indexOf(key) == -1) {
            document.getElementById("address").value += location_data[key] + ", "
          }
        }
      });
    });
  } else {
    alert("Geolocation is not supported by this browser.");
  } 
}

function get_chat_history(event_id) {
  fetch("https://1ptsftnwde.execute-api.us-east-1.amazonaws.com/test/get_chat_history?event_id=" + event_id, {
      method: 'GET'
    }).then(response => response.json())
    .then(data => {
      var c_j = check_cookie();
      var uid = c_j["user_data"]["email"];
      events = data["body"];
      console.log(events)
      for(idx in events) {
          let evnt = events[idx];
          console.log(evnt)
          temp_chat_box = `
          <a href="#" class="list-group-item list-group-item-action">
          <div class="d-flex w-100 justify-content-between">
        `
        if (evnt["user_id"] === uid || evnt["user_id"] == c_j["user_data"]["user_id"]) {
          temp_chat_box += '<h5 class="mb-1">You</h5>'
        } else {
          temp_chat_box += '<h5 class="mb-1">' + evnt["given_name"] + '</h5>'
        }
        var dt = new Date(+evnt["timestamp"] * 1000);
        temp_chat_box += '<small class="text-muted">' + dt.toDateString() + "  " + dt.toLocaleTimeString() + '</small></div>'
        temp_chat_box += '<p class="mb-1">' + evnt["message"] + '</p></a>'
        $("#chat").append(temp_chat_box);
      }
      $("#chat").children().last()[0].scrollIntoView();
    });
}

function get_location() {
  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(position => {
      lat = (position.coords.latitude).toString()
      long = (position.coords.longitude).toString()
    });
  } else {
    alert("Geolocation is not supported by this browser.");
  } 
}

function search_query() {
  data = {
    "query": document.getElementById("query").value,
    "online_event": ( $("#type").val() === "online" ),
    "category": $("#categories").val(),
  }
  if(typeof(lat) != 'undefined') {
    data["location"] = {
      "lat": lat,
      "lon": long
    }
  }
  console.log(data)
  url = "https://pbfg5ityf0.execute-api.us-east-1.amazonaws.com/default/RenderSearch" 
  // data["query"] + "&online_event=" + JSON.stringify(data["online_event"]) + "&category=" + data["category"]
  // + "&lat=" + data["lat"] + "&long=" + data["long"]
  fetch(url, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  })
  .then(response => response.json())
  .then(data => {
    document.close();
    document.open();
    document.write(data["body"])
    document.close();
  })
  .catch((error) => {
    // window.location.href = "/event_failure.html"
    console.log(error);
  });
}