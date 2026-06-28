# -*- coding: utf-8 -*-
"""
Created on Sun Mar  9 22:42:34 2025

@author: WANG ZIAN
"""

import xml.etree.ElementTree as ET
import pandas as pd

def parse_xpx(file_path):
    """ Parses an .xpx file and extracts D1 & D2 values """

    # Load XML file
    tree = ET.parse(file_path)
    root = tree.getroot()

    # Locate the <rawData> section
    raw_data_element = root.find(".//rawData")
    if raw_data_element is None:
        print("No <rawData> found! Check XML structure.")
        return None

    # Extract all rows from <rawData>
    raw_text = raw_data_element.text.strip()
    raw_rows = raw_text.split("\n")  # Split into lines

    # Define relevant column indices (26 to 36)
    target_columns = {
        26: "D1_32Hz_R", 27: "D1_32Hz_Theta", 28: "D1_100Hz_R", 29: "D1_100Hz_Theta", 33: "D2_32Hz_R", 34: "D2_32Hz_Theta", 35: "D2_100Hz_R", 36: "D2_100Hz_Theta"
    }

    # Parse data rows
    data_list = []
    for row in raw_rows:
        values = row.strip().split()  # Split by spaces
        if len(values) < 37:  # Ensure there are enough columns
            continue
        
        # Extract only required columns
        extracted_values = {target_columns[i]: float(values[i]) for i in target_columns}
        data_list.append(extracted_values)

    # Convert to DataFrame
    df = pd.DataFrame(data_list)
    return df

# Run Parser
file_path = "C:/pipeline_diagnostics/Sample Data 1/Analyzed Data/2025-08-07-002.xpx"
df = parse_xpx(file_path)
if df is not None:
    print(df.head())  # Preview extracted data
else:
    print("Parsing failed! No data extracted.")
df.to_csv("87002_D1D2_parsed.txt", sep="\t", index=False)
