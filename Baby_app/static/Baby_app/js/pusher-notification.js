const beamsClient = new PusherPushNotifications.Client({
    instanceId: "624dc809-45e5-4a7e-bd92-f36425957490",
  });
beamsClient
.start()
.then((beamsClient) => beamsClient.getDeviceId())
.then((deviceId) =>
    console.log("Successfully registered with Beams. Device ID:", deviceId)
)
.then(() => beamsClient.addDeviceInterest("BVP-user-1"))
.then(() => beamsClient.getDeviceInterests())
.then((interests) => console.log("Current push notification interests:", interests))
.catch(console.error);