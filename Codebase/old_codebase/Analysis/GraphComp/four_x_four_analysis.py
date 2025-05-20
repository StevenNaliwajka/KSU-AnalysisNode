import sys
from datetime import datetime
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from Codebase.Pathing.get_analysis_folder import get_analysis_folder
from Codebase.Pathing.get_raw_photos import get_raw_photos


def four_x_four_analysis(analysis_script: str, output_path: str, comp_1: str, comp_1_id: str, comp_2: str, comp_2_id: str) -> None:
    analysis_folder = get_analysis_folder()
    raw_folder = get_raw_photos()

    output_folder = Path(output_path).parent
    output_folder.mkdir(parents=True, exist_ok=True)

    variations = [
        (1, 1),
        (1, 2),
        (2, 1),
        (2, 2),
    ]

    image_paths = []

    for tvws_instance, soil_moisture_instance in variations:
        img_filename = f"{comp_1}_vs_{comp_2}_{tvws_instance}_{soil_moisture_instance}.png"
        img_path = raw_folder / img_filename

        command = [
            "python3",  # Directly call python3
            str(analysis_folder / analysis_script),
            str(tvws_instance),
            str(soil_moisture_instance),
            str(comp_1),
            str(comp_1_id),
            str(comp_2),
            str(comp_2_id),
            str(img_path)
        ]

        try:
            subprocess.run(command, check=True)
            image_paths.append(img_path)
        except subprocess.CalledProcessError as e:
            print(f"Error running script for TVWS={tvws_instance}, Soil={soil_moisture_instance}: {e}")

    if len(image_paths) != 4:
        print("Error: Not all images were generated. Exiting.")
        return

    images = [Image.open(img) for img in image_paths]

    width, height = images[0].size
    label_space_x = 60
    label_space_y = 60

    combined_width = width * 2 + label_space_x
    combined_height = height * 2 + label_space_y
    combined_image = Image.new("RGB", (combined_width, combined_height), "white")

    try:
        font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 36)
    except OSError:
        print("Warning: Could not load DejaVuSans font. Falling back to default font.")
        font = ImageFont.load_default()

    draw = ImageDraw.Draw(combined_image)

    positions = [
        (label_space_x, label_space_y),
        (label_space_x + width, label_space_y),
        (label_space_x, label_space_y + height),
        (label_space_x + width, label_space_y + height)
    ]
    for img, pos in zip(images, positions):
        combined_image.paste(img, pos)

    column_labels = ["Soil: -6\"", "Soil: -1\""]
    for i, label in enumerate(column_labels):
        text_width = font.getbbox(label)[2]
        x = label_space_x + i * width + (width - text_width) // 2
        y = 10
        draw.text((x, y), label, fill="black", font=font)

    row_labels = ["TVWS: -6\" Buried", "TVWS: Tower"]
    for i, label in enumerate(row_labels):
        y = label_space_y + i * height + height // 2
        x = 20

        text_width, text_height = font.getbbox(label)[2:]
        text_img = Image.new("RGBA", (text_width, text_height), (255, 255, 255, 0))
        text_draw = ImageDraw.Draw(text_img)
        text_draw.text((0, 0), label, fill="black", font=font)

        rotated_text = text_img.rotate(90, expand=True)
        bbox = rotated_text.getbbox()
        if bbox:
            rotated_text = rotated_text.crop(bbox)

        adjusted_x = x
        adjusted_y = y - rotated_text.height // 2
        combined_image.paste(rotated_text, (adjusted_x, adjusted_y), rotated_text)

    combined_image.save(output_path)
    print(f"Combined image saved at {output_path}")


if __name__ == "__main__":
    args = sys.argv[1:]
    req_value = 6
    if len(args) < req_value:
        print(f"Error: Not enough arguments provided. Expected {req_value} values.")
        sys.exit(1)

    analysis_script, output_path, comp_1, comp_1_id, comp_2, comp_2_id = args[:6]
    four_x_four_analysis(analysis_script, output_path, comp_1, comp_1_id, comp_2, comp_2_id)
