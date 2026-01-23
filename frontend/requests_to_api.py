import httpx


base_url = "http://localhost:8000"


def base_response(func):
    async def wrapper(*args):
        data = None

        try:
            response = await func(*args)

            if response.status_code == 200:
                data = response.json()
                print({"message": "Request successful", "data": data})
            else:
                print({"message": "Request failed"})
        except:
            print({"message": "Request impossible"})

        return data

    return wrapper


@base_response
async def get_all_products():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{base_url}/api/products")
    return response


@base_response
async def get_products_by_id(ids: list[int]):
    for id in ids:
        print(f"{id} packed to request")

    async with httpx.AsyncClient() as client:
        response = await client.get(f"{base_url}/api/products/by_ids", params={f"ids": ids})
        print(response.url)

    return response


@base_response
async def get_products_by_user_token(token: str):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{base_url}/api/products/by_token", params={f"token": token})
        print(response.url)

    return response



@base_response
async def post_order(products: dict[int: int]):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{base_url}/api/products/order", data=products)

    return response


@base_response
async def try_register(username: str, password: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{base_url}/api/register", data={"username": username, "password": password})

    return response


@base_response
async def try_login(username: str, password: str):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{base_url}/api/login", data={"username": username, "password": password})

    return response


@base_response
async def try_post_product(name, seller_token, price, count):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{base_url}/api/products/post", data={
            "name": name,
            "seller_token": seller_token,
            "price": price,
            "count": count
        })

    return response
