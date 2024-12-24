import gradio as gr
import os
import glob
import exifread
from iptcinfo3 import IPTCInfo

# Extract EXIF metadata
def extract_exif_metadata(filename):
    with open(filename, 'rb') as img_file:
        tags = exifread.process_file(img_file, stop_tag="EXIF UserComment")
        exif_data = {}
        for tag in tags.keys():
            exif_data[tag] = str(tags[tag])
        return exif_data

# Extract IPTC metadata
def extract_iptc_metadata(filename):
    try:
        info = IPTCInfo(filename, force=True)
        return info.data
    except Exception as e:
        return {}

# Perform alternative license searches
def alternative_license_search(exif_data, iptc_data):
    possible_license_keywords = ['license', 'rights', 'usage rights', 'legal', 'copyright', 'cc']
    possible_license = None

    for tag, value in exif_data.items():
        for keyword in possible_license_keywords:
            if keyword in tag.lower() or keyword in str(value).lower():
                possible_license = value
                break
        if possible_license:
            break

    if not possible_license:
        for tag, value in iptc_data.items():
            for keyword in possible_license_keywords:
                if keyword in str(tag).lower() or keyword in str(value).lower():
                    possible_license = value
                    break
            if possible_license:
                break

    return possible_license

# Check for different types of licenses
def check_license(exif_data, iptc_data):
    license_type = None

    if 'EXIF UserComment' in exif_data:
        comment = exif_data['EXIF UserComment'].lower()
        if 'creativecommons' in comment:
            license_type = 'Creative Commons'
        elif 'public domain' in comment:
            license_type = 'Public Domain'
        elif 'royalty-free' in comment:
            license_type = 'Royalty-Free'

    if not license_type and 'copyright' in iptc_data:
        copyright_info = str(iptc_data['copyright']).lower()
        if 'creativecommons' in copyright_info:
            license_type = 'Creative Commons'
        elif 'public domain' in copyright_info:
            license_type = 'Public Domain'
        elif 'royalty-free' in copyright_info:
            license_type = 'Royalty-Free'
        elif 'all rights reserved' in copyright_info:
            license_type = 'All Rights Reserved'

    return license_type

# Main function to process uploaded images
def process_images(files=None, url=None):
    results = []
    license_summary = {
        'No License Found': 0,
        'Creative Commons': 0,
        'Public Domain': 0,
        'Royalty-Free': 0,
        'All Rights Reserved': 0,
        'Possible License Found (Alternative)': 0
    }

    if files:
        for file in files:
            filename = file.name
            file_path = os.path.join("/tmp", filename)
            
            if hasattr(file, 'read'):
                with open(file_path, "wb") as f:
                    f.write(file.read())
            else:
                with open(file_path, "wb") as f:
                    f.write(file.encode('utf-8'))

            exif_data = extract_exif_metadata(file_path)
            iptc_data = extract_iptc_metadata(file_path)
            license_type = check_license(exif_data, iptc_data)

            if not license_type:
                possible_license = alternative_license_search(exif_data, iptc_data)
                if possible_license:
                    license_type = 'Possible License Found (Alternative)'

            if license_type:
                license_summary[license_type] += 1
            else:
                license_summary['No License Found'] += 1

            results.append(f"File: {filename} - License: {license_type if license_type else 'No License Found'}")

    if url:
        results.append("URL analysis not implemented yet")

    summary = "\nLicense Summary:\n"
    for license_type, count in license_summary.items():
        summary += f"{license_type}: {count} images\n"

    return "\n".join(results) + summary

# Gradio interface
with gr.Blocks() as interface:
    gr.Markdown("# Image License Inspector 🔍")
    gr.Markdown("## The Image License Inspector allows you to upload images and inspect their metadata for potential licenses such as Creative Commons, Public Domain, and others.")
    gr.Markdown("### Version 1 developed by Ramon Mayor Martins, 2024 | [Personal Website](https://rmayormartins.github.io/) | [Hugging Face Spaces](https://huggingface.co/rmayormartins)")

    with gr.Row():
        with gr.Column():
            files = gr.File(file_count="multiple", label="Upload Images")
            url = gr.Textbox(label="Or provide an image URL")

        output = gr.Textbox(label="Results")

    submit_button = gr.Button("Inspect")
    submit_button.click(process_images, inputs=[files, url], outputs=output)

interface.launch()
