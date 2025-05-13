import cv2
import os
import numpy as np
from pdf2image import convert_from_path
from pypdf import PdfReader
import pytesseract

class ResumeReader:
    """
    A class to read and process resume files from specified directories.
    """
    # CREATE A SINGLETON INSTANCE
    _instance = None
    _resume_data = None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(ResumeReader, cls).__new__(cls)
        return cls._instance

    @staticmethod
    def extract_text_from_pdf(file):
        reader = PdfReader(file)
        data = ""
        for page in reader.pages:
            data = data + page.extract_text() + "\n"
        data = data.strip().lower()
        return data

    def extract_text_from_image(self, file):
        pages = convert_from_path(file)
        extracted_text = []
        for page in pages:
            # Step 1: Preprocess the image (deskew)
            preprocessed_image = self.deskew(np.array(page))
            # Step 2: Extract text using OCR
            text = self.get_text_from_image(preprocessed_image)
            extracted_text.append(text)
        return "\n".join(extracted_text).strip().lower()

    def read_resume_data(self, resume_path):
        """
        Reads resume files from the specified directory and stores the content in resume_data attribute.
        If the resume file is a PDF containing images, OCR is used to extract text.

        Returns:
            dict: A dictionary with resume identifiers as keys and the corresponding resume texts as values.
        """
        if not os.path.isfile(resume_path):
            raise FileNotFoundError(f"Resume file not found: {resume_path}")
            
        data = self.extract_text_from_pdf(resume_path)
        if len(data) > 1:
            self._resume_data = data
        else:  # to solve for incorrect startxref pointer(3), since they are images in pdf
            self._resume_data = self.extract_text_from_image(resume_path)
        return self._resume_data

    @staticmethod
    def deskew(image):
        """
       Deskews the given image to correct any tilt.

       Args:
           image (numpy.ndarray): The image to be deskewed.

       Returns:
           numpy.ndarray: The deskewed image.
       """
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        gray = cv2.bitwise_not(gray)
        coords = np.column_stack(np.where(gray > 0))
        angle = cv2.minAreaRect(coords)[-1]

        if angle < -45:
            angle = -(90 + angle)
        else:
            angle = -angle

        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        return rotated

    @staticmethod
    def get_text_from_image(image):
        """
       Extracts text from the given image using OCR.

       Args:
           image (numpy.ndarray): The image from which to extract text.

       Returns:
           str: The extracted text.
       """
        text = pytesseract.image_to_string(image)
        return text
