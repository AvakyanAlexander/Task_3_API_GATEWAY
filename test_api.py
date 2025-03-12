import pytest
import httpx


@pytest.fixture(scope="module")
def global_header():
    token_in_header = {"Authorization": ""}
    return token_in_header


@pytest.fixture(scope="module")
def global_fields():
    connect_fields = {
        "contract_id": "",
        "document_id": ""
    }
    return connect_fields


@pytest.mark.asyncio
async def test_auth_get_token(global_header):
    data = {
        "username": "admin",
        "password": "admin",
    }
    async with httpx.AsyncClient(base_url="http://127.0.0.1:8000") as client:
        response = await client.post("/token", data=data)
        response_json = response.json()
        token = response_json["access_token"]
        assert response.status_code == 200
        global_header["Authorization"] = f"Bearer {token}"


@pytest.mark.asyncio
async def test_upload_file(global_header, global_fields):
    # загрузка файла
    test_file = ("test_file.txt", b"test content")

    async with httpx.AsyncClient(base_url="http://127.0.0.1:8000") as client:
        response = await client.post(
            "/api/v1/DBO/upload/",
            files={"file": test_file},
            headers=global_header
        )
        response_json = response.json()
        assert response.status_code == 200
        assert response_json["msg"] == "Документ успешно загружен"
        global_fields["document_id"] = response_json["doc_id"]


@pytest.mark.asyncio
async def test_get_client_documents(global_header):
    async with httpx.AsyncClient(base_url="http://127.0.0.1:8000") as client:
        response = await client.get("/api/v1/ABS/client_documents/",
                                    headers=global_header)
        assert response.status_code == 200
        response_json = response.json()
        assert "contract_list" in response_json
        assert isinstance(response_json["contract_list"], list)


@pytest.mark.asyncio
async def test_create_contract(global_fields, global_header):
    data = {
        "name": "Потребительский кредит",
        "desc": "Контракт на получение потребительского кредита на сумму до 500,000 рублей на срок до 5 лет. Платежи по кредиту фиксированы.",
    }

    async with httpx.AsyncClient(base_url="http://127.0.0.1:8000") as client:
        response = await client.post(
            "/api/v1/SM/create_contract",
            params=data,
            headers=global_header
        )
        responce_json = response.json()
        assert response.status_code == 200
        global_fields["contract_id"] = responce_json["con_id"]


@pytest.mark.asyncio
async def test_connect_contract_document(global_fields, global_header):

    data = {
        "contract_idd": int(global_fields["contract_id"]),
        "document_idd": int(global_fields["document_id"])
    }

    async with httpx.AsyncClient(base_url="http://127.0.0.1:8000") as client:
        response = await client.post(
            "/api/v1/SM/connect_contract_document",
            params=data,
            headers=global_header
        )
        print(data)
        response_json = response.json()
        print(response_json)
        assert response.status_code == 200
        assert response_json["msg"] == "Документ успешно привязан к контракту"
