def pinghealthcheck():
    import os
    import requests

    uuid = os.getenv('HEALTHCHECK_UUID')
    if not uuid:
        print("HEALTHCHECK_UUID is not set in the env, skipping ping.")
        return

    url = f'https://hc-ping.com/{uuid}'
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("Health check successful.")
        else:
            print(f"Health check failed with status code: {response.status_code}")
    except requests.RequestException as e:
        print(f"An error occurred during the health check: {e}")