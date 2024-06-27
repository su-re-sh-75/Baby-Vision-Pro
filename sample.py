import pusher

app_id = "1824386"
key = "a5728f3261909ddf0eba"
secret = "d9673b39c593cecc21f8"
cluster = "ap2"

pusher_client = pusher.Pusher(
        app_id=app_id,
        key=key,
        secret=secret,
        cluster=cluster
    )
pusher_client.trigger('sensor-data-channel', 'sensor-data-event', {'message': 'hello world'})