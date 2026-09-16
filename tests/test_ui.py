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


def test_decimal_point_is_limited_to_each_number() -> None:
    ui = CalculatorUI.__new__(CalculatorUI)
    ui.current_input = ""
    ui.display_var = FakeDisplay()

    for value in "1.2.3+4.5.6":
        ui._append_to_input(value)

    assert ui.current_input == "1.23+4.56"
    assert ui.display_var.value == "1.23+4.56"