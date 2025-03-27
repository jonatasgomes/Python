import requests
from bs4 import BeautifulSoup

def decode_secret_message(doc_url):
    # Fetch the Google Doc content
    response = requests.get(doc_url)
    if response.status_code != 200:
        print("Failed to fetch the document")
        return
    
    # Parse the HTML content
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find all table rows (skip the header row)
    rows = soup.find_all('tr')[1:]  # Skip header row
    
    # Initialize variables to store data and track grid dimensions
    grid_data = []
    max_x = 0
    max_y = 0
    
    for row in rows:
        cells = row.find_all('td')
        if len(cells) >= 3:
            try:
                x = int(cells[0].get_text(strip=True))
                char = cells[1].get_text(strip=True)
                y = int(cells[2].get_text(strip=True))
                
                grid_data.append((x, y, char))
                
                # Update max coordinates
                if x > max_x:
                    max_x = x
                if y > max_y:
                    max_y = y
            except ValueError:
                continue
    
    # Create an empty grid filled with spaces
    grid = [[' ' for _ in range(max_x + 1)] for _ in range(max_y + 1)]
    
    # Fill in the characters
    for x, y, char in grid_data:
        if y < len(grid) and x < len(grid[y]):
            grid[y][x] = char
    
    # Print the grid row by row
    for row in grid:
        print(''.join(row))

# Test the function with the provided URL
decode_secret_message("https://docs.google.com/document/d/e/2PACX-1vQGUck9HIFCyezsrBSnmENk5ieJuYwpt7YHYEzeNJkIb9OSDdx-ov2nRNReKQyey-cwJOoEKUhLmN9z/pub")
