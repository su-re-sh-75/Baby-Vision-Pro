const firebaseConfig = {
  apiKey: "AIzaSyAQV1Jjxc0PR5vezin1izte7efO9Cclh20",
  authDomain: "baby-vision-pro.firebaseapp.com",
  projectId: "baby-vision-pro",
  storageBucket: "baby-vision-pro.appspot.com",
  messagingSenderId: "517430442063",
  appId: "1:517430442063:web:bae629ad7fe86471f8123a",
  measurementId: "G-DKPSCQTMZ3"
};

// Initialize Firebase
const app = firebase.initializeApp(firebaseConfig);
const analytics = firebase.analytics();
const messaging = firebase.messaging();
// Add the public key generated from the console here.
messaging.getToken(messaging, {vapidKey: "BC-7jNFQAWck7Rqljk1YTyhxtWHTFUUafMoLWxEaQ7hoUfRZWaYpa05ewyaUnXg5eptFlv8G58B7N2Hsgqt4_qY"}).then((currentToken) => {
  if (currentToken) {
    console.log(currentToken)
    fetch('/store_token/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        subscription: currentToken
      })
    }).then(response => response.text())
      .then(data => console.log(data));
  } else {
    console.log('No registration token available. Request permission to generate one.');
  }
}).catch((err) => {
  console.log('An error occurred while retrieving token. ', err);
});

messaging.requestPermission().then(function(){
  console.log('Notification permission granted.');
  return messaging.getToken();
}).catch(function(err){
  console.log('Unable to get permission to notify: ', err);
});

messaging.onMessage((payload)=>{
  console.log("Message received: ", payload);
})