from src.auth import check_password


def test_correct_password():
    assert check_password("admin123") is True


def test_wrong_password():
    assert check_password("wrongpassword") is False