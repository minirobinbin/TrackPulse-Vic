def pinghealthcheck():
    import os
    import requests

    uuid = os.getenv('HEALTHCHECK_UUID')

    url = f'https://hc-ping.com/{uuid}'
    
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print("Health check successful.")
        else:
            print(f"Health check failed with status code: {response.status_code}, check the UUID is set correctly in the env")
    except requests.RequestException as e:
        print(f"An error occurred during the health check: {e}")
        
pinghealthcheck()