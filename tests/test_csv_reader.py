import pytest

from brand_rate.reader import CSVProductReader


def make_csv(tmp_path, name, rows):
    path = tmp_path / name
    header = "name,brand,price,rating\n"
    content = header + "\n".join(rows) + "\n"
    path.write_text(content, encoding="utf-8")
    return path


def test_read_many_combines_multiple_files(tmp_path):
    file_a = make_csv(
        tmp_path,
        "a.csv",
        [
            "n1,apple,10,4.4",
        ],
    )
    file_b = make_csv(
        tmp_path,
        "b.csv",
        [
            "n2,samsung,20,4.2",
            "n3,xiaomi,30,4.1",
        ],
    )

    reader = CSVProductReader()
    records = reader.read_many([file_a, file_b])

    assert len(records) == 3
    assert {record.name for record in records} == {"n1", "n2", "n3"}


def test_read_many_requires_at_least_one_file():
    reader = CSVProductReader()
    with pytest.raises(ValueError):
        reader.read_many([])


def test_read_missing_file_raises_error():
    reader = CSVProductReader()
    with pytest.raises(FileNotFoundError):
        reader.read("does-not-exist.csv")
