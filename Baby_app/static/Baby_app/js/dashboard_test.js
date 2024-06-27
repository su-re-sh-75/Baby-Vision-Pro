var pusher = new Pusher("a5728f3261909ddf0eba", {
    cluster: "ap2",
});
var channel = pusher.subscribe("sensor-data-channel");
console.log('subscribed to sensor-data-channel in channels');
channel.bind("sensor-data-event", (data) => {
    process_sensor_data(data);
});
function process_sensor_data(data){
    console.log(data.message);
};