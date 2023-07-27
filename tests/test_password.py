from cibo.password import Password


def test_hash_and_verify():
    hasher = Password()

    hashed_password = hasher.hash_("abc123")

    assert hasher.verify("abc123", hashed_password) is True
