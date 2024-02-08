import difflib
import io
import pathlib
import tempfile

from click.testing import CliRunner
from tola.assembly.scripts.pretext_to_tpf import cli


def test_example_data():
    # Examples in order of increasing complexity
    for specimen in (
        "iyExeIsch1",
        "idDilFebr1",
        "nxCaeSini1_1",
        "idSyrVitr1",
        "ngHelPoly1_1",
        "eaAstIrre1",
        "bChlMac1_3",
        "ilIthSala1_1",
    ):
        data_dir = pathlib.Path(__file__).parent / "data"
        run_assembly(data_dir, specimen)


def run_assembly(data_dir, specimen):
    specimen_dir = data_dir / specimen
    input_tpf = f"{specimen}-input.tpf"
    pretext_agp = f"{specimen}-pretext.agp"
    assert (specimen_dir / input_tpf).exists()
    assert (specimen_dir / pretext_agp).exists()

    output_tpf = f"{specimen}-pretext-to-tpf.tpf"
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = pathlib.Path(str(tmp_dir))
        args = (
            "--assembly",
            specimen_dir / input_tpf,
            "--pretext",
            specimen_dir / pretext_agp,
            "--output",
            tmp_path / output_tpf,
            "--write-log",
        )
        runner = CliRunner()
        result = runner.invoke(cli, args)
        assert result.exit_code == 0
        for spec_path in specimen_dir.iterdir():
            spec_file = spec_path.name
            if spec_file in (input_tpf, pretext_agp) or spec_file.startswith("."):
                # Skip the input and hidden files
                continue
            test_path = tmp_path / spec_file
            print(f"Specimen dir file: {spec_file}")
            assert test_path.exists()
            diff_files(specimen, spec_path, test_path)


def diff_files(specimen, spec_path, test_path):
    ctx_diff = difflib.context_diff(
        spec_path.open("r").readlines(),
        test_path.open("r").readlines(),
        fromfile=f"{specimen}/{spec_path.name}",
        tofile=f"test/{test_path.name}",
    )
    str_io = io.StringIO()
    str_io.writelines(ctx_diff)
    ctx_str = str_io.getvalue()
    if ctx_str:
        print(ctx_str)
    assert ctx_str == ""


if __name__ == "__main__":
    test_example_data()
