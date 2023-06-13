import allure
import requests
from pydantic import BaseModel


def validate_request_json(json: str | BaseModel):
    if isinstance(json, dict):
        return json
    return json.dict(by_alias=True, exclude_none=True)


def validate_status_code(response: requests.Response, status_code: int):
    with allure.step("Проверка валидации и статус кода"):
        assert response.status_code == status_code, f'Status code of response should be equal status_code but equals {response.status_code}'
