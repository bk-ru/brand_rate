import csv

import pytest

import main


def write_products_file(tmp_path, name, rows):
    path = tmp_path / name
    header = "name,brand,price,rating\n"
    path.write_text(header + "\n".join(rows) + "\n", encoding="utf-8")
    return path


def test_cli_prints_average_rating_table(tmp_path, capsys):
    file_one = write_products_file(
        tmp_path,
        "first.csv",
        [
            "iphone,Apple,1000,4.9",
            "galaxy,Samsung,900,4.6",
        ],
    )
    file_two = write_products_file(
        tmp_path,
        "second.csv",
        [
            "redmi,Xiaomi,500,4.2",
            "iphone se,Apple,600,4.1",
        ],
    )

    exit_code = main.run(
        ["--files", str(file_one), str(file_two), "--report", "average-rating"]
    )

    captured = capsys.readouterr()

    assert exit_code == 0
    assert "apple" in captured.out
    assert "samsung" in captured.out
    assert "+----" in captured.out  # границы таблицы


def test_cli_fails_when_file_missing(capsys):
    with pytest.raises(SystemExit) as exc_info:
        main.run(["--files", "missing.csv", "--report", "average-rating"])

    assert exc_info.value.code == 2
    captured = capsys.readouterr()
    assert "Ошибка" in captured.err
    assert "--files" in captured.out


def test_cli_accepts_directory_input(tmp_path):
    data_dir = tmp_path / "inputs"
    data_dir.mkdir()
    write_products_file(
        data_dir,
        "one.csv",
        [
            "iphone,Apple,1000,4.9",
        ],
    )
    write_products_file(
        data_dir,
        "two.csv",
        [
            "galaxy,Samsung,900,4.6",
        ],
    )

    exit_code = main.run(["--path", str(data_dir), "--report", "average-rating"])

    assert exit_code == 0


def test_cli_save_flag_writes_csv(tmp_path):
    file_path = write_products_file(
        tmp_path,
        "items.csv",
        [
            "iphone,Apple,1000,4.9",
            "iphone se,Apple,600,4.1",
        ],
    )
    output_path = tmp_path / "out" / "report.csv"

    main.run(
        [
            "--files",
            str(file_path),
            "--report",
            "average-rating",
            "--save",
            str(output_path),
        ]
    )

    with output_path.open(encoding="utf-8") as file_obj:
        reader = csv.DictReader(file_obj)
        rows = list(reader)

    assert reader.fieldnames == ["brand", "rating"]
    assert rows == [{"brand": "apple", "rating": "4.5"}]


def test_cli_errors_when_directory_missing(capsys):
    with pytest.raises(SystemExit) as exc_info:
        main.run(["--path", "no_such_dir", "--report", "average-rating"])

    assert exc_info.value.code == 2
    captured = capsys.readouterr()
    assert "Ошибка" in captured.err
    assert "--path" in captured.out


def test_cli_help_flag_prints_usage(capsys):
    with pytest.raises(SystemExit) as exc_info:
        main.run(["--help"])

    assert exc_info.value.code == 0
    captured = capsys.readouterr()
    assert "--files" in captured.out
    assert "--report" in captured.out
