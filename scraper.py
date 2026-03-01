import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_shl():
    # SHL Product Catalog ka main URL [cite: 38]
    url = "https://www.shl.com/solutions/products/product-catalog/"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
    
    try:
        print("SHL Catalog load ho raha hai...")
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        results = []
        
        # Sabhi links nikalna [cite: 53]
        links = soup.find_all('a', href=True)
        # Sirf wo links jo products ki taraf jate hain
        test_links = [l['href'] for l in links if '/product-catalog/view/' in l['href']]
        
        # Duplicate links hatayein
        test_links = list(set(test_links))
        print(f"{len(test_links)} potential tests mile hain.")

        # Kam se kam 377 tests ka data chahiye [cite: 54]
        # Hum pehle 377 links ka data process karenge
        for link in test_links[:377]: 
            if not link.startswith('http'):
                link = "https://www.shl.com" + link
            
            # Name nikalne ke liye URL ko clean karein
            test_name = link.split('/')[-2].replace('-', ' ').title()
            
            results.append({
                "Name": test_name,
                "URL": link,
                "Description": f"{test_name} assessment for screening candidates.",
                "Duration": 30, # Default duration
                "Test Type": "General Knowledge & Skills" # Default type [cite: 113]
            })
            
        if len(results) > 0:
            df = pd.DataFrame(results)
            # Data ko CSV mein save karein [cite: 74, 78]
            df.to_csv("shl_tests_data.csv", index=False)
            print(f"SUCCESS: {len(results)} tests ka data 'shl_tests_data.csv' mein save ho gaya hai!")
        else:
            print("Koi tests nahi mile. Website structure check karein.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    scrape_shl()