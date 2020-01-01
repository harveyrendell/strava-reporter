from discord.handler import respond_to_challenge


def test_200_response_to_valid_challenge():
    response = respond_to_challenge(
        {"queryStringParameters": {"hub.challenge": "123456"}}
    )

    assert response["statusCode"] == 200
    assert response["body"] == '{"hub.challenge": "123456"}'


def test_400_response_to_invalid_challenge():
    response = respond_to_challenge(
        {"queryStringParameters": {"hub.unchallenge": "123456"}}
    )

    assert response["statusCode"] == 400
    assert response["body"] == "Invalid request"
