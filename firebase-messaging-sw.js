importScripts("https://www.gstatic.com/firebasejs/8.10.0/firebase-app.js");
importScripts("https://www.gstatic.com/firebasejs/8.10.0/firebase-messaging.js");
var firebaseConfig = { 
        apiKey: "AIzaSyAQV1Jjxc0PR5vezin1izte7efO9Cclh20", 
        authDomain: "baby-vision-pro.firebaseapp.com", 
        projectId: "baby-vision-pro", 
        storageBucket: "baby-vision-pro.appspot.com", 
        messagingSenderId: "517430442063", 
        appId: "1:517430442063:web:bae629ad7fe86471f8123a", 
        measurementId: "G-DKPSCQTMZ3" 
}; 
firebase.initializeApp(firebaseConfig); 
const messaging=firebase.messaging(); 
messaging.setBackgroundMessageHandler(function (payload) { 
    console.log(payload); 
    const notification=JSON.parse(payload); 
    const notificationOption={ 
        body:notification.body, 
        icon:notification.icon 
    }; 
    return self.registration.showNotification(payload.notification.title,notificationOption); 
});