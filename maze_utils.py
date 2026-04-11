"""Utility helpers for configuration and output file management."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Tuple

Coordinate = Tuple[int, int]


class ConfigError(ValueError):
    """Raised when configuration is invalid or cannot be loaded."""


@dataclass
class MazeConfig:
    """Store validated configuration values for maze generation."""

    width: int
    height: int
    entry: Coordinate
    exit: Coordinate
    output_file: str
    perfect: bool
    seed: Optional[int]
    interactive: bool
    show_path: bool


def _parse_bool(text: str, key_name: str) -> bool:
    """Parse a boolean-like string value."""
    normalized = text.strip().lower()
    if normalized in {"true", "1", "yes", "on"}:
        return True
    if normalized in {"false", "0", "no", "off"}:
        return False
    raise ConfigError(f"{key_name} must be a boolean (True or False).")


def _parse_coordinate(text: str, key_name: str) -> Coordinate:
    """Parse coordinates in x,y format."""
    parts = [part.strip() for part in text.split(",")]
    if len(parts) != 2:
        raise ConfigError(f"{key_name} must use x,y format.")

    try:
        x_value = int(parts[0])
        y_value = int(parts[1])
    except ValueError as error:
        raise ConfigError(
            f"{key_name} must contain integer coordinates."
        ) from error

    return (x_value, y_value)


def _parse_int(text: str, key_name: str) -> int:
    """Parse a required integer value."""
    try:
        return int(text.strip())
    except ValueError as error:
        raise ConfigError(f"{key_name} must be an integer.") from error


def _read_key_values(config_path: str) -> Dict[str, str]:
    """Read KEY=VALUE pairs from config file."""
    entries: Dict[str, str] = {}
    path = Path(config_path)

    if not path.exists():
        raise ConfigError(f"Config file not found: {config_path}")

    try:
        lines = path.read_text(encoding="utf-8").splitlines()
    except OSError as error:
        raise ConfigError(f"Cannot read config file: {config_path}") from error

    for line_index, raw_line in enumerate(lines, start=1):
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if "=" not in line:
            raise ConfigError(
                f"Invalid config line {line_index}: expected KEY=VALUE format."
            )

        key, value = line.split("=", 1)
        normalized_key = key.strip().upper()
        if not normalized_key:
            raise ConfigError(f"Invalid empty key at line {line_index}.")
        entries[normalized_key] = value.strip()

    return entries


def _validate_bounds(config: MazeConfig) -> None:
    """Ensure dimensions and coordinates are coherent."""
    if config.width <= 0 or config.height <= 0:
        raise ConfigError("WIDTH and HEIGHT must be positive integers.")

    def is_inside(point: Coordinate) -> bool:
        x_coord, y_coord = point
        return 0 <= x_coord < config.width and 0 <= y_coord < config.height

    if not is_inside(config.entry):
        raise ConfigError("ENTRY must be inside maze bounds.")
    if not is_inside(config.exit):
        raise ConfigError("EXIT must be inside maze bounds.")
    if config.entry == config.exit:
        raise ConfigError("ENTRY and EXIT must be different.")


def load_config(config_path: str) -> MazeConfig:
    """Load and validate maze configuration from file."""
    values = _read_key_values(config_path)

    required_keys = {
        "WIDTH",
        "HEIGHT",
        "ENTRY",
        "EXIT",
        "OUTPUT_FILE",
        "PERFECT",
    }

    missing = sorted(required_keys - set(values.keys()))
    if missing:
        missing_text = ", ".join(missing)
        raise ConfigError(f"Missing mandatory config key(s): {missing_text}")

    width = _parse_int(values["WIDTH"], "WIDTH")
    height = _parse_int(values["HEIGHT"], "HEIGHT")
    entry = _parse_coordinate(values["ENTRY"], "ENTRY")
    exit_point = _parse_coordinate(values["EXIT"], "EXIT")
    output_file = values["OUTPUT_FILE"].strip()
    perfect = _parse_bool(values["PERFECT"], "PERFECT")

    if not output_file:
        raise ConfigError("OUTPUT_FILE cannot be empty.")

    seed: Optional[int] = None
    if "SEED" in values and values["SEED"].strip():
        seed = _parse_int(values["SEED"], "SEED")

    interactive = False
    if "INTERACTIVE" in values:
        interactive = _parse_bool(values["INTERACTIVE"], "INTERACTIVE")

    show_path = False
    if "SHOW_PATH" in values:
        show_path = _parse_bool(values["SHOW_PATH"], "SHOW_PATH")

    config = MazeConfig(
        width=width,
        height=height,
        entry=entry,
        exit=exit_point,
        output_file=output_file,
        perfect=perfect,
        seed=seed,
        interactive=interactive,
        show_path=show_path,
    )

    _validate_bounds(config)
    return config


def write_output_file(
    output_file: str,
    hex_rows: List[str],
    entry: Coordinate,
    exit_point: Coordinate,
    path_steps: List[str],
) -> None:
    """Write maze and metadata to output file in subject format."""
    lines: List[str] = []
    lines.extend(hex_rows)
    lines.append("")
    lines.append(f"{entry[0]},{entry[1]}")
    lines.append(f"{exit_point[0]},{exit_point[1]}")
    lines.append("".join(path_steps))

    payload = "\n".join(lines) + "\n"

    try:
        Path(output_file).write_text(payload, encoding="utf-8")
    except OSError as error:
        raise ConfigError(
            f"Unable to write output file: {output_file}"
        ) from error
