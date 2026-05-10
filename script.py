import requests
import pandas as pd
import re # This is the Regular Expression library

url = 'https://greenvalley.pk/collections/snacks/products.json?limit=50'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    raw_data = response.json()
    products_list = []
    
    for item in raw_data['products']:
        title = item['title']
        price = float(item['variants'][0]['price'])
        
        # Updated Regex to catch 'oz' and the typo '0z'
        weight_match = re.search(r'(?i)(\d+\.?\d*)\s*(gm|g|ml|kg|oz|0z)', title)
        
        if weight_match:
            weight_value = float(weight_match.group(1))
            unit = weight_match.group(2).lower()
            
            # --- STANDARDIZATION LOGIC ---
            if unit == 'kg':
                weight_in_grams = weight_value * 1000
            elif unit in ['oz', '0z']:
                weight_in_grams = weight_value * 28.35
            else:
                weight_in_grams = weight_value # Already in g/gm/ml
        else:
            weight_value = None
            unit = None
            weight_in_grams = None

        products_list.append({
            'Product Name': title,
            'Price (PKR)': price,
            'Weight': weight_value,
            'Unit': unit,
            'Weight_Grams': weight_in_grams
        })
        
    df = pd.DataFrame(products_list)
    
    # Now the math is consistent!
    df['Price_Per_Gram'] = df['Price (PKR)'] / df['Weight_Grams']
    
    print("\nCleaned Data:")
    # We'll show the top 10 items so you can see the results
    print(df[['Product Name', 'Price (PKR)', 'Weight', 'Unit', 'Weight_Grams', 'Price_Per_Gram']].head(10))

    from datetime import date
    filename = f"greenvalley_snacks_{date.today()}.csv"
    df.to_csv(filename, index=False)
