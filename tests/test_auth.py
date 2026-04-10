# def test_register_and_login(client):
#     register_response = client.post(
#         "/register",
#         # можно передать просто json
#         json={
#             "username": "test_user_1",
#             "password": "testpassword123"
#         }
#     )
#
#     assert register_response.status_code in (200, 201)
#
#     login_response = client.post(
#         "/login",
#         # OAuth2PasswordRequestForm ждет form-data
#         data = {
#             "username": "test_user_1",
#             "password": "testpassword123"
#         }
#     )
#
#     assert login_response.status_code == 200
#
#     data = login_response.json()
#     assert "access_token" in data
#     assert data["token_type"] == "bearer"