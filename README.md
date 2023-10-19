# Strava webhook


## Documentation:
* Authentication flow: https://developers.strava.com/docs/authentication/
* Webhooks: https://developers.strava.com/docs/webhooks/
* Webhook design: https://birdie0.github.io/discord-webhooks-guide/

## Run

#### Install dependencies

```shell script
npm install
```

#### Set up secrets file

Create a secrets file for your specific stage: `.env.<stage>`
Include the following variables.
```shell script
CLIENT_ID=<value>
CLIENT_SECRET=<value>
DISCORD_WEBHOOK_URL=<value>
LAYER_ARN=<value>
MAPBOX_ACCESS_TOKEN=<value>
```

#### Deploy with serverless

```shell script
serverless deploy --stage <stage>
```

## Setting up a Strava subscription

Steps to set up a Strava subscription are defined [here](https://developers.strava.com/docs/webhooks/)
(You must get approval before your application will receive events).

```shell script
curl -X POST https://api.strava.com/api/v3/push_subscriptions \
      -F client_id=<client-id> \
      -F client_secret=<client-secret> \
      -F 'callback_url=https://<your-callback-url>' \
      -F 'verify_token=STRAVA'
```

## Developing

To deploy a single function:

```shell script
serverless deploy function --stage <stage> --function <function-name>
```