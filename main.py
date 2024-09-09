import pandas as pd
from bs4 import BeautifulSoup

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

# Usage
df = extract_kindle_highlights('example-100Moffers.html')
save_to_csv(df, 'kindle_highlights.csv')
