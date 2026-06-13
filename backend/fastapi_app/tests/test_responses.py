from fastapi_app.utils.responses import ApiError, ApiResponse, ErrorDetail, MetaData


def test_api_response_ok_defaults() -> None:
    resp = ApiResponse.ok(data={"key": "value"})
    assert resp.success is True
    assert resp.message == "Success"
    assert resp.data == {"key": "value"}
    assert resp.errors is None


def test_api_response_created() -> None:
    resp = ApiResponse.created(data={"id": 1}, message="User created")
    assert resp.success is True
    assert resp.message == "User created"
    assert resp.data == {"id": 1}


def test_api_response_with_meta() -> None:
    meta = MetaData(page=1, page_size=10, total=100, total_pages=10)
    resp = ApiResponse.ok(data=[], meta=meta)
    assert resp.meta is not None
    assert resp.meta.total == 100


def test_api_error_not_found() -> None:
    err = ApiError.not_found("Post")
    assert err.success is False
    assert "Post" in err.message
    assert err.data is None


def test_api_error_validation() -> None:
    errors = [ErrorDetail(field="email", message="Invalid email")]
    err = ApiError.validation_error(errors)
    assert err.success is False
    assert err.errors is not None
    assert err.errors[0].field == "email"


def test_api_error_unauthorized() -> None:
    err = ApiError.unauthorized()
    assert err.success is False
    assert "Authentication" in err.message


def test_api_error_forbidden() -> None:
    err = ApiError.forbidden()
    assert err.success is False
    assert "permission" in err.message.lower()
