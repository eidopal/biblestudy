def handler(request, response):
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "text/plain"
        },
        "body": "Hello from Vercel Function (alternate style)!"
    } 