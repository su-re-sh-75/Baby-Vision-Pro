import pusher

app_id = "<pusher-app-id>"
key = "<pusher-key>"
secret = "<pusher-secret>"
cluster = "<cluster-id>"

pusher_client = pusher.Pusher(
        app_id=app_id,
        key=key,
        secret=secret,
        cluster=cluster
    )
pusher_client.trigger('sensor-data-channel', 'sensor-data', {'message': 'hello world'})