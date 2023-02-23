def test_get_all_post(authorized_client):
    res = authorized_client.get("/posts/")
    print(res.json())
    assert res.status_code == 200
