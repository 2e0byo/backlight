"""Extremely simple backlight control script."""

from argparse import ArgumentParser
from pathlib import Path

ROOT = Path("/sys/class/backlight")


def get_best_backlight():
    return next(d for d in ROOT.glob("*") if d.is_dir())


def max_brightness(backlight: Path) -> float:
    return int((backlight / "max_brightness").read_text())


def get_brightness(backlight: Path) -> float:
    return int((backlight / "brightness").read_text()) / max_brightness(backlight)


def set_brightness(backlight: Path, brightness: float):
    (backlight / "brightness").write_text(
        str(round(max_brightness(backlight) * brightness))
    )


def main():
    parser = ArgumentParser()
    parser.add_argument("brightness", nargs="?", help="Brightness to set.", type=float)
    parser.add_argument("--backlight", help="Which backlight to set.")
    parser.add_argument(
        "--as-float",
        help="Print current brightness as a float.",
        action="store_true",
    )
    args = parser.parse_args()
    backlight = ROOT / (args.backlight or get_best_backlight())
    if not backlight.exists():
        raise ValueError(f"No such backlight: {backlight}")
    if args.brightness:
        set_brightness(backlight, args.brightness)

    if args.as_float:
        print(get_brightness(backlight))
    else:
        print(f"{get_brightness(backlight):2.0%}")


if __name__ == "__main__":
    main()
