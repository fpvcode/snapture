import os
import pytest
from snapture import mksnap, unsnap, hash  # Додано імпорт хешу


@pytest.fixture
def setup_test_dirs(tmpdir):
    # Create a test structure
    input_dir = tmpdir.mkdir("input")
    output_dir = tmpdir.mkdir("output")
    snap_file = tmpdir.join("structure.snap")

    # Add files to the input directory
    input_dir.join("test_file.txt").write("This is a test file.")
    input_dir.mkdir("subdir").join("nested_file.txt").write("Nested file content.")

    return str(input_dir), str(output_dir), str(snap_file)


def test_snap_and_unsnap(setup_test_dirs):
    input_dir, output_dir, snap_file = setup_test_dirs

    # Test the creation of a snap file
    mksnap(input_dir, snap_file)

    # Check whether the snap file exists
    assert os.path.exists(snap_file)

    # Test the unsnap
    unsnap(snap_file, output_dir)

    # Check whether the files in the output directory have been restored
    assert os.path.exists(os.path.join(output_dir, "test_file.txt"))
    assert os.path.exists(os.path.join(output_dir, "subdir", "nested_file.txt"))

    # Check the contents of the restored files
    with open(os.path.join(output_dir, "test_file.txt")) as f:
        restored_content = f.read()
        assert restored_content == "This is a test file."

    with open(os.path.join(output_dir, "subdir", "nested_file.txt")) as f:
        restored_content = f.read()
        assert restored_content == "Nested file content."

    # Check the hashes of the restored files
    assert hash(os.path.join(output_dir, "test_file.txt")) == hash(os.path.join(input_dir, "test_file.txt"))
    assert hash(os.path.join(output_dir, "subdir", "nested_file.txt")) == hash(
        os.path.join(input_dir, "subdir", "nested_file.txt"))
