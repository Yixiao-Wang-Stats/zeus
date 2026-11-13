"""Export selected camera-ready PDF figures as web images; leave sources untouched."""
from pathlib import Path
import subprocess
import tempfile
from PIL import Image

root = Path(__file__).resolve().parents[1]
source = root / "orginal paper" / "figures"
destination = root / "static" / "media"
destination.mkdir(parents=True, exist_ok=True)
figures = {
    "extrapolation_story": "approximation-schemes",
    "p1": "ablation-predictor-lpips",
    "p2": "ablation-predictor-mse",
    "p3": "ablation-reuse",
    "p4": "ablation-consecutive-steps",
}
with tempfile.TemporaryDirectory(prefix="zeus-figures-") as temporary:
    for name, exported_name in figures.items():
        prefix = Path(temporary) / name
        subprocess.run([
            "pdftoppm", "-f", "1", "-singlefile", "-scale-to", "1800", "-png",
            str(source / f"{name}.pdf"), str(prefix)
        ], check=True)
        with Image.open(prefix.with_suffix(".png")) as figure:
            figure.convert("RGB").save(destination / f"{exported_name}.webp", quality=95)
        print(f"Exported {exported_name}.webp")
