import os
from pypdf import PdfReader
from PIL import Image

pdf_path = r"C:\Users\aftab\.gemini\antigravity\brain\55f21c69-9f27-4b4e-ad1e-712b00ff105b\.user_uploaded\media_1793302001192_71cc90de.pdf"
out_dir = r"docs\report_assets"
os.makedirs(out_dir, exist_ok=True)

reader = PdfReader(pdf_path)
print(f"Total pages: {len(reader.pages)}")

# Extract images from page 1 and page 2 (logo)
for p_idx in [0, 1, 6]:
    page = reader.pages[p_idx]
    count = 0
    for image_file_object in page.images:
        out_name = f"page_{p_idx+1}_img_{count}_{image_file_object.name}"
        out_path = os.path.join(out_dir, out_name)
        with open(out_path, "wb") as fp:
            fp.write(image_file_object.data)
        print(f"Saved {out_path}")
        count += 1
