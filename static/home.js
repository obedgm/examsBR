// Initialize Firebase
var config = {
  	apiKey: "AIzaSyCMs1O70z1q6qIArA36dBX1iuipaNStOYg",
  	authDomain: "examsbr-2a061.firebaseapp.com",
  	databaseURL: "https://examsbr-2a061.firebaseio.com",
  	projectId: "examsbr-2a061",
  	storageBucket: "",
  	messagingSenderId: "1086622454733"
	};
	firebase.initializeApp(config);
	var clicked = false;
	function onSignIn(googleUser) {
    var f = document.createElement("form");
    var profile = googleUser.getBasicProfile();
    f.setAttribute('method',"post");
    f.setAttribute('action',"/login");
    f.style.display = "none";
    document.body.appendChild(f);
    if (clicked) {
    	f.submit();
    }
}