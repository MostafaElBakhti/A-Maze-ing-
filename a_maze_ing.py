"""Main entrypoint for A-Maze-ing."""

from __future__ import annotations

import random
import sys
import time
from typing import List, Optional, Tuple

from maze_generator import MazeGenerator
from maze_utils import ConfigError, MazeConfig, load_config, write_output_file
from visualizer import AsciiVisualizer

Coordinate = Tuple[int, int]


def _build_generator(config: MazeConfig, seed: Optional[int]) -> MazeGenerator:
    """Create and run maze generator from config."""
    generator = MazeGenerator(
        width=config.width,
        height=config.height,
        entry=config.entry,
        exit_=config.exit,
        is_perfect=config.perfect,
        seed=seed,
    )
    generator.generate()
    return generator


def _generate_and_write(
    config: MazeConfig,
    seed: Optional[int],
) -> Tuple[MazeGenerator, List[str]]:
    """Generate maze, compute shortest path and write output file."""
    generator = _build_generator(config, seed)
    path_steps = generator.shortest_path()
    write_output_file(
        output_file=config.output_file,
        hex_rows=generator.to_hex_rows(),
        entry=config.entry,
        exit_point=config.exit,
        path_steps=path_steps,
    )
    return generator, path_steps


def _print_usage() -> None:
    """Print command usage."""
    print("Usage: python3 a_maze_ing.py config.txt")


def _clear_screen() -> None:
    """Clear terminal screen using ANSI escape sequences."""
    print("\033[2J\033[H", end="")


def _print_menu() -> str:
    """Print interactive menu and return selected command."""
    print("=== A-Maze-ing Menu ===")
    print("1. Regenerate New Maze")
    print("2. Change Colors")
    print("3. Animate Path Finding")
    print("Q. Quit")
    return input("Choose (1/2/3/Q): ").strip().upper()


def _animate_path_finding(
    visualizer: AsciiVisualizer,
    path_steps: List[str],
    palette_index: int,
    seed_value: Optional[int],
    warnings: List[str],
) -> None:
    """Animate shortest path discovery by revealing path step by step."""
    if not path_steps:
        _clear_screen()
        visualizer.display(
            show_path=True,
            palette_index=palette_index,
            generation_seed=seed_value,
            warnings=warnings,
        )
        return

    for step_count in range(1, len(path_steps) + 1):
        visualizer.path_steps = path_steps[:step_count]
        _clear_screen()
        visualizer.display(
            show_path=True,
            palette_index=palette_index,
            generation_seed=seed_value,
            warnings=warnings,
        )
        time.sleep(0.04)

    visualizer.path_steps = path_steps


def _interactive_loop(
    config: MazeConfig,
    generator: MazeGenerator,
    path_steps: List[str],
    seed_in_use: Optional[int],
) -> int:
    """Run terminal controls with menu options."""
    palette_index = 0
    seed_value = seed_in_use

    while True:
        visualizer = AsciiVisualizer(generator, path_steps)
        _clear_screen()
        visualizer.display(
            show_path=config.show_path,
            palette_index=palette_index,
            generation_seed=seed_value,
            warnings=generator.warnings,
        )

        command = _print_menu()

        if command == "1":
            if seed_value is None:
                seed_value = random.randint(0, 10_000_000)
            else:
                seed_value += 1

            try:
                generator, path_steps = _generate_and_write(config, seed_value)
                print(f"Maze regenerated and saved to {config.output_file}.")
                time.sleep(0.6)
            except (ConfigError, RuntimeError, ValueError) as error:
                print(f"Error: {error}")
                return 1
        elif command == "2":
            palette_index += 1
        elif command == "3":
            _animate_path_finding(
                visualizer=visualizer,
                path_steps=path_steps,
                palette_index=palette_index,
                seed_value=seed_value,
                warnings=generator.warnings,
            )
            input("Press Enter to continue...")
        elif command == "Q":
            return 0
        else:
            print("Unknown command. Please use 1, 2, 3, or Q.")
            time.sleep(0.8)


def main() -> int:
    """Program entrypoint."""
    if len(sys.argv) != 2:
        _print_usage()
        return 1

    config_path = sys.argv[1]

    try:
        config = load_config(config_path)
        active_seed = config.seed
        generator, path_steps = _generate_and_write(config, active_seed)

        print(f"Maze written to {config.output_file}")

        if config.interactive:
            return _interactive_loop(
                config,
                generator,
                path_steps,
                active_seed,
            )

        visualizer = AsciiVisualizer(generator, path_steps)
        visualizer.display(
            show_path=config.show_path,
            palette_index=0,
            generation_seed=active_seed,
            warnings=generator.warnings,
        )

        return 0
    except (ConfigError, RuntimeError, ValueError) as error:
        print(f"Error: {error}")
        return 1
    except Exception as error:  # pragma: no cover
        print(f"Error: unexpected failure: {error}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
