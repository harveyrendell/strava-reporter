# Strava webhook


### Documentation:
* Authentication flow: https://developers.strava.com/docs/authentication/
* Webhooks: https://developers.strava.com/docs/webhooks/
* Webhook design: https://birdie0.github.io/discord-webhooks-guide/

# Install

npm install

# Run

## Deploy serverless

```bash
serverless deploy --client_id <client-id> --client_secret <client-secret>
```

## Setting up a Strava subscription

Steps to set up a Strava subscription are defined [here](https://developers.strava.com/docs/webhooks/)
(You must get approval before your application will receive events).

```bash
curl -X POST https://api.strava.com/api/v3/push_subscriptions \
      -F client_id=<client-id> \
      -F client_secret=<client-secret> \
      -F 'callback_url=https://<your-callback-url>' \
      -F 'verify_token=STRAVA'
```