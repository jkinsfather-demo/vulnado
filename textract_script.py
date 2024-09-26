import boto3
import os
import zipfile

# Initialize AWS Textract client
client = boto3.client('textract')

def extract_text_from_image(image_file):
    with open(image_file, 'rb') as img:
        img_bytes = img.read()
    response = client.detect_document_text(Document={'Bytes': img_bytes})
    detected_text = ""
    for block in response['Blocks']:
        if block['BlockType'] == 'LINE':
            detected_text += block['Text'] + "\n"
    return detected_text

def process_images_in_folder(root_folder):
    print("Entered process_images_in_folder")
    image_extensions = ['.png', '.jpg', '.jpeg', '.tiff', '.bmp']
    text_files = []
    for foldername, subfolders, filenames in os.walk(root_folder):
        for filename in filenames:
            ext = os.path.splitext(filename)[1].lower()
            if ext in image_extensions:
                image_path = os.path.join(foldername, filename)
                print(f"Processing: {image_path}")
                extracted_text = extract_text_from_image(image_path)
                txt_filename = f"im2txt-{os.path.splitext(filename)[0]}.txt"
                txt_filepath = os.path.join(foldername, txt_filename)
                text_files.append(txt_filepath)
                with open(txt_filepath, 'w') as txt_file:
                    txt_file.write(extracted_text)
                print(f"Text written to: {txt_filepath}")
    return text_files

def create_zip_of_txt_files(text_files, zip_filename):
    with zipfile.ZipFile(zip_filename, 'w') as zipf:
        for txt_file in text_files:
            zipf.write(txt_file, os.path.basename(txt_file))
            print(f"Added {txt_file} to zip.")

root_folder = 'text_in_images'
zip_filename = 'im2txt_output.zip'
text_files = process_images_in_folder(root_folder)
create_zip_of_txt_files(text_files, zip_filename)
print(f"All text files zipped into: {zip_filename}")
