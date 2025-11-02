from PIL import Image
import os
import glob
import random
def combine_cards(card1_path, card2_path, output_path):
    card1 = Image.open(card1_path).convert("RGBA")
    card2 = Image.open(card2_path).convert("RGBA")
    if card1.height != card2.height:
        common_height = min(card1.height, card2.height)
        card1 = card1.resize((int(card1.width * common_height / card1.height), common_height))
        card2 = card2.resize((int(card2.width * common_height / card2.height), common_height))
    combined_width = card1.width + card2.width
    combined = Image.new("RGBA", (combined_width, card1.height))
    combined.paste(card1, (0, 0), card1)
    combined.paste(card2, (card1.width, 0), card2)
    combined.save(output_path)
    print(f"Saved: {output_path}")
input_folder = os.path.dirname(os.path.abspath(__file__))
paths = sorted(
    glob.glob(os.path.join(input_folder, "*.png")) +
    glob.glob(os.path.join(input_folder, "*.jpg")) +
    glob.glob(os.path.join(input_folder, "*.jpeg"))
)
if len(paths) < 2:
    print("Not enough images to process.")
    exit()
random.shuffle(paths)
if len(paths) % 2 != 0:
    skipped = random.choice(paths)
    print(f"Odd number of images detected. Skipping: {os.path.basename(skipped)}")
    paths.remove(skipped)
output_folder = os.path.join(input_folder, "battles")
os.makedirs(output_folder, exist_ok=True)
for i in range(0, len(paths), 2):
    card1 = paths[i]
    card2 = paths[i + 1]
    name1 = os.path.splitext(os.path.basename(card1))[0]
    name2 = os.path.splitext(os.path.basename(card2))[0]
    output_name = f"{name1}_vs_{name2}.png"
    output_path = os.path.join(output_folder, output_name)
    combine_cards(card1, card2, output_path)
print(f"\nAll images saved to: {output_folder}")
