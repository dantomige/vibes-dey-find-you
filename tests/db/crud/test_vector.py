import torch
import pytest

from src.db.crud.vector import VectorDBRepository  # change this import


# -------------------------
# Helpers
# -------------------------

def rand_vec(dim=384):
    return torch.randn(dim)


# -------------------------
# Tests
# -------------------------

def test_add_and_get_vector():
    db = VectorDBRepository()

    vec = rand_vec()

    db.add_vector("song_1", vec)
    retrieved = db.get_vector("song_1")

    assert retrieved is not None
    assert isinstance(retrieved, torch.Tensor)
    assert torch.allclose(retrieved, vec, atol=1e-5)


def test_get_missing_vector():
    db = VectorDBRepository()

    assert db.get_vector("missing") is None


def test_update_overwrites_vector():
    db = VectorDBRepository()

    v1 = rand_vec()
    v2 = rand_vec()

    db.add_vector("song_2", v1)
    db.update_vector("song_2", v2)

    retrieved = db.get_vector("song_2")

    assert retrieved is not None
    assert torch.allclose(retrieved, v2, atol=1e-5)


def test_delete_vector():
    db = VectorDBRepository()

    vec = rand_vec()

    db.add_vector("song_3", vec)
    db.remove_vector("song_3")

    assert db.get_vector("song_3") is None


def test_search_returns_results():
    db = VectorDBRepository()

    db.add_vector("song_a", rand_vec())
    db.add_vector("song_b", rand_vec())
    db.add_vector("song_c", rand_vec())

    query = rand_vec()

    results = db.search(query, k=2)

    assert "ids" in results
    assert len(results["ids"][0]) <= 2


def test_search_self_match():
    db = VectorDBRepository()

    vec = rand_vec()

    db.add_vector("song_self", vec)

    results = db.search(vec, k=1)

    assert results["ids"][0][0] == "song_self"


def test_duplicate_add_behavior():
    db = VectorDBRepository()

    v1 = rand_vec()
    v2 = rand_vec()

    db.add_vector("song_x", v1)
    db.add_vector("song_x", v2)

    retrieved = db.get_vector("song_x")

    assert retrieved is not None


def test_bulk_insert_and_search():
    db = VectorDBRepository()

    for i in range(50):
        db.add_vector(f"song_{i}", rand_vec())

    results = db.search(rand_vec(), k=10)

    assert len(results["ids"][0]) == 10


def test_update_missing_vector_behavior():
    db = VectorDBRepository()

    vec = rand_vec()

    db.update_vector("missing_song", vec)

    # depending on chroma behavior, this should now exist or be handled
    retrieved = db.get_vector("missing_song")

    assert retrieved is not None