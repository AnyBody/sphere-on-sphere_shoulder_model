from anypytools import AnyPyProcess, macro_commands as mc

from pathlib import Path

model_path = Path(__file__).parent.parent / "GH_2spheres.main.any"

def test_model():
    app = AnyPyProcess()

    macro = [
        mc.Load(model_path),
        mc.OperationRun("Main.RunApplication"),
        #mc.Dump("<some variable we can then later check>")
    ]

    result = app.start_macro(macro)[0]

    # TODO: Add test code to check results and dumped variables
    # For example, you can check if the expected output is in the result
    # and if the dumped variables contain the expected values.

    if "ERROR" in result:
        raise RuntimeError("Model simulation failed: " + str(result["ERROR"]))

