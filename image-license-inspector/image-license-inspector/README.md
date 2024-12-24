---
title: image-license-inspector
emoji: 🔍🪪
colorFrom: blue
colorTo: green
sdk: gradio
sdk_version: "4.12.0"
app_file: app.py
pinned: false
---

# Image License Inspector 🔍

The Image License Inspector is a tool that allows you to upload images (.jpg, .png, .bmp, etc.) and inspect them for metadata, including potential licenses such as Creative Commons, Public Domain, Royalty-Free, and others.

## How It Works

This tool processes images and extracts metadata using EXIF, IPTC, and alternative keyword searches to identify licenses. You can either upload images, provide a URL, or point to a Google Drive folder to analyze your images.

### Example Use Cases

1. **Upload images**: Upload multiple images to check their licenses.
2. **Provide a URL**: Enter a URL to analyze the image (not fully implemented).
3. **Google Drive folder**: Provide the path to a folder in your Google Drive with images to analyze.

## Project Overview

This project is designed to inspect image metadata and extract information about potential licenses. The tool checks for licenses like Creative Commons, Public Domain, Royalty-Free, and others by analyzing EXIF and IPTC metadata.

## Technical Details

The project utilizes the following libraries:
- **ExifRead** for EXIF metadata extraction.
- **IPTCInfo3** for IPTC metadata extraction.

## Developer Information

Developed by Ramon Mayor Martins (2024).

Email: rmayormartins@gmail.com  
GitHub: https://github.com/rmayormartins  
Homepage: https://rmayormartins.github.io/





