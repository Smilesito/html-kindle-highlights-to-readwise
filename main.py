import pandas as pd
from bs4 import BeautifulSoup
import os

def extract_kindle_highlights(html_file):
    with open(html_file, 'r', encoding='utf-8') as file:
        soup = BeautifulSoup(file, 'html.parser')

    book_title = soup.find('div', class_='bookTitle').text.strip()
    author = soup.find('div', class_='authors').text.strip()
    highlights = []
    for note in soup.find_all('div', class_='noteText'):
        text = note.text.strip()
        location = note.find_previous('div', class_='noteHeading').text
        location = int(''.join(filter(str.isdigit, location)))
        highlights.append({'Highlight': text, 'Location': location})

    df = pd.DataFrame(highlights)
    df['Title'] = book_title
    df['Author'] = author
    return df[['Title', 'Author', 'Location', 'Highlight']]

def save_to_csv(df, output_file):
    df.to_csv(output_file, index=False)
    print(f"CSV file saved as {output_file}")

def process_folder(input_folder, output_file):
    all_highlights = []
    for filename in os.listdir(input_folder):
        if filename.endswith('.html'):
            html_file = os.path.join(input_folder, filename)
            df = extract_kindle_highlights(html_file)
            all_highlights.append(df)
    
    if all_highlights:
        combined_df = pd.concat(all_highlights, ignore_index=True)
        save_to_csv(combined_df, output_file)
        print(f"Processed {len(all_highlights)} files.")
    else:
        print("No HTML files found in the specified folder.")

# Usage
input_folder = '/Users/sergiorueda/dev/html-kindle-highlights-to-readwise/to-process'
output_file = 'all'
process_folder(input_folder, output_file)
