from dataclasses import dataclass

# dataclass skriver __init__ automatiskt
# frozen=True gör instansen immutable
@dataclass(frozen=True)
class ReportConfig:
    input_file: str
    output_folder: str


DEFAULT_CONFIG = ReportConfig(
    input_file="data/orders.csv",
    output_folder="output",
)