import sys
from datetime import datetime
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

from Codebase.Pathing.get_analysis_folder import get_analysis_folder
from Codebase.Pathing.get_python_venv_exec_path import get_python_venv_exec_path
from Codebase.Pathing.get_raw_photos import get_raw_photos


def four_x_four_analysis(analysis_script:str, output_path:str, comp_1:str, comp_1_id:str, comp_2:str, comp_2_id:str) -> None:
    # gen paths
    analysis_folder = get_analysis_folder()
    raw_folder = get_raw_photos()

    # Path to venv python
    venv_python = get_python_venv_exec_path()

    output_folder = Path(output_path).parent
    # Ensure output folder exists
    output_folder.mkdir(parents=True, exist_ok=True)


    # Variation. Hardcoded to 2x2
    variations = [
        (1, 1),
        (1, 2),
        (2, 1),
        (2, 2),
    ]

    # img pths
    image_paths = []

    # run 4 times
    for tvws_instance, soil_moisture_instance in variations:
        img_filename = f"{comp_1}_vs_{comp_2}_{tvws_instance}_{soil_moisture_instance}.png"
        img_path = raw_folder / img_filename

        command = [
            str(venv_python),
            str(analysis_folder / analysis_script),
            str(tvws_instance),
            str(soil_moisture_instance),
            str(comp_1),
            str(comp_1_id),
            str(comp_2),
            str(comp_2_id),
            str(raw_folder / img_filename)
        ]
        # tvws_num: int, moisture_num: int, var_1: str, var_2: str, output_path: str

        try:
            subprocess.run(command, check=True)
            image_paths.append(img_path)
        except subprocess.CalledProcessError as e:
            print(f"Error running script for TVWS={tvws_instance}, Soil={soil_moisture_instance}: {e}")

    # Check for pics
    if len(image_paths) != 4:
        print("Error: Not all images were generated. Exiting.")
        return

    images = [Image.open(img) for img in image_paths]

    # Ensure images are the same size
    width, height = images[0].size
    label_space_x = 60
    label_space_y = 60

    # Create a new image with extra space for labels
    combined_width = width * 2 + label_space_x
    combined_height = height * 2 + label_space_y
    combined_image = Image.new("RGB", (combined_width, combined_height), "white")

    # Load font
    font_path = "C:/Windows/Fonts/arial.ttf"
    font = ImageFont.truetype(font_path, 36)

    # Create a drawing context
    draw = ImageDraw.Draw(combined_image)

    # Add images to the canvas
    positions = [
        (label_space_x, label_space_y),  # Top-left image (TVWS=1, Soil=1)
        (label_space_x + width, label_space_y),  # Top-right image (TVWS=1, Soil=2)
        (label_space_x, label_space_y + height),  # Bottom-left image (TVWS=2, Soil=1)
        (label_space_x + width, label_space_y + height)  # Bottom-right image (TVWS=2, Soil=2)
    ]
    for img, pos in zip(images, positions):
        combined_image.paste(img, pos)

    # Add **centered** column labels (Soil moisture)
    column_labels = ["Soil: -6\"", "Soil: -1\""]
    for i, label in enumerate(column_labels):
        text_width = font.getbbox(label)[2]  # Get width of the text
        x = label_space_x + i * width + (width - text_width) // 2  # Proper centering
        y = 10  # Near the top
        draw.text((x, y), label, fill="black", font=font)

    # Add rotated row labels (TVWS)
    row_labels = ["TVWS: -6\" Buried", "TVWS: Tower"]
    for i, label in enumerate(row_labels):
        y = label_space_y + i * height + height // 2  # Center vertically
        x = 20  # Move labels closer to images

        # Get text size properly
        text_width, text_height = font.getbbox(label)[2:]  # Correct method

        # Create a new blank image for rotated text (transparent background)
        text_img = Image.new("RGBA", (text_width, text_height), (255, 255, 255, 0))
        text_draw = ImageDraw.Draw(text_img)
        text_draw.text((0, 0), label, fill="black", font=font)

        # Rotate and properly crop the text
        rotated_text = text_img.rotate(90, expand=True)
        bbox = rotated_text.getbbox()  # Crop to actual text size
        if bbox:
            rotated_text = rotated_text.crop(bbox)

        # Adjust positioning to **reduce whitespace**
        adjusted_x = x  # Keep aligned to the left margin
        adjusted_y = y - rotated_text.height // 2  # Center vertically

        # Paste the rotated text onto the combined image
        combined_image.paste(rotated_text, (adjusted_x, adjusted_y), rotated_text)

    # Save final image
    combined_image.save(output_path)
    print(f"Combined image saved at {output_path}")

if __name__ == "__main__":
    args = sys.argv[1:]
    req_value = 6
    if len(args) < req_value:
        print(f"Error: Not enough arguments provided. Expected {req_value} values.")
        sys.exit(1)

    analysis_script, output_path, comp_1, comp_1_id, comp_2, comp_2_id= args[:6]
    four_x_four_analysis(analysis_script, output_path, comp_1, comp_1_id, comp_2, comp_2_id)
