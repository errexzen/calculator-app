from ui import CalculatorUI


class FakeDisplay:
    def __init__(self) -> None:
        self.value = ""

    def set(self, value: str) -> None:
        self.value = value


def test_clear_resets_input_and_display() -> None:
    ui = CalculatorUI.__new__(CalculatorUI)
    ui.current_input = "12.5+3"
    ui.display_var = FakeDisplay()

    ui.clear()

    assert ui.current_input == ""
    assert ui.display_var.value == "0"