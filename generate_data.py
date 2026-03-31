import pandas as pd
import numpy as np

np.random.seed(42)

brands = ['Dell', 'HP', 'Lenovo', 'Apple', 'Asus', 'Acer', 'MSI', 'Microsoft', 'Razer', 'Samsung']
processors = ['Intel Core i3', 'Intel Core i5', 'Intel Core i7', 'Intel Core i9',
              'AMD Ryzen 3', 'AMD Ryzen 5', 'AMD Ryzen 7', 'AMD Ryzen 9', 'Apple M1', 'Apple M2']

# Generation per processor family (realistic 2024 market)
processor_generations = {
    'Intel Core i3': ['10th Gen', '11th Gen', '12th Gen', '13th Gen'],
    'Intel Core i5': ['10th Gen', '11th Gen', '12th Gen', '13th Gen', '14th Gen'],
    'Intel Core i7': ['11th Gen', '12th Gen', '13th Gen', '14th Gen'],
    'Intel Core i9': ['12th Gen', '13th Gen', '14th Gen'],
    'AMD Ryzen 3': ['Ryzen 5000', 'Ryzen 6000', 'Ryzen 7000'],
    'AMD Ryzen 5': ['Ryzen 5000', 'Ryzen 6000', 'Ryzen 7000'],
    'AMD Ryzen 7': ['Ryzen 5000', 'Ryzen 6000', 'Ryzen 7000'],
    'AMD Ryzen 9': ['Ryzen 6000', 'Ryzen 7000'],
    'Apple M1': ['M1', 'M1 Pro', 'M1 Max'],
    'Apple M2': ['M2', 'M2 Pro', 'M2 Max'],
}

ram_options = [4, 8, 16, 32, 64]
storage_types = ['HDD', 'SSD', 'Hybrid']
storage_sizes = [256, 512, 1024, 2048]
screen_sizes = [13.3, 14.0, 15.6, 17.3]
gpu_types = ['Integrated', 'NVIDIA GTX 1650', 'NVIDIA RTX 3050', 'NVIDIA RTX 3060',
             'NVIDIA RTX 3070', 'NVIDIA RTX 4060', 'AMD Radeon']
os_types = ['Windows 10', 'Windows 11', 'macOS', 'Linux']
weights = [1.2, 1.5, 1.8, 2.0, 2.3, 2.5]

n_samples = 1000

processor_col = np.random.choice(processors, n_samples)
generation_col = [np.random.choice(processor_generations[p]) for p in processor_col]

data = {
    'Brand': np.random.choice(brands, n_samples),
    'Processor': processor_col,
    'Generation': generation_col,
    'RAM_GB': np.random.choice(ram_options, n_samples),
    'Storage_Type': np.random.choice(storage_types, n_samples),
    'Storage_GB': np.random.choice(storage_sizes, n_samples),
    'Screen_Size': np.random.choice(screen_sizes, n_samples),
    'GPU': np.random.choice(gpu_types, n_samples),
    'OS': np.random.choice(os_types, n_samples),
    'Weight_kg': np.random.choice(weights, n_samples),
    'Touchscreen': np.random.choice([0, 1], n_samples, p=[0.7, 0.3]),
    'Warranty_Years': np.random.choice([1, 2, 3], n_samples, p=[0.5, 0.3, 0.2])
}

df = pd.DataFrame(data)

# Real 2024 Indian market prices (Amazon/Flipkart aligned)
def calculate_price(row):
    # Realistic base prices per processor (matches actual market listings)
    processor_base = {
        'Intel Core i3': 25000,   # Dell/Acer i3 base ~25k
        'Intel Core i5': 38000,   # Dell Inspiron i5 ~38k
        'Intel Core i7': 58000,   # HP/Dell i7 ~58k
        'Intel Core i9': 95000,   # Dell XPS i9 ~95k
        'AMD Ryzen 3': 23000,
        'AMD Ryzen 5': 35000,
        'AMD Ryzen 7': 55000,
        'AMD Ryzen 9': 88000,
        'Apple M1': 92000,        # MacBook Air M1 ~92k
        'Apple M2': 112000,       # MacBook Air M2 ~1.12L
    }
    base_price = processor_base.get(row['Processor'], 45000)

    # Generation premium — newer gen costs more
    gen_premium = {
        '10th Gen': -2000, '11th Gen': 0, '12th Gen': 2000,
        '13th Gen': 4000,  '14th Gen': 6000,
        'Ryzen 5000': 0, 'Ryzen 6000': 2000, 'Ryzen 7000': 4000,
        'M1': 0, 'M1 Pro': 20000, 'M1 Max': 45000,
        'M2': 0, 'M2 Pro': 28000, 'M2 Max': 55000,
    }
    base_price += gen_premium.get(row['Generation'], 0)

    # Brand premium/discount (real market positioning)
    brand_delta = {
        'Apple': 8000, 'Microsoft': 5000, 'Razer': 10000,
        'MSI': 3000,   'Samsung': 2000,   'Dell': 0,
        'HP': 0,       'Asus': 0,         'Lenovo': -1000, 'Acer': -2000
    }
    base_price += brand_delta.get(row['Brand'], 0)

    # RAM — extra cost only above 8GB baseline
    base_price += (row['RAM_GB'] - 8) * 400

    # Storage type
    storage_add = {'HDD': 0, 'Hybrid': 1500, 'SSD': 3000}
    base_price += storage_add.get(row['Storage_Type'], 0)
    if row['Storage_GB'] == 512:  base_price += 1500
    elif row['Storage_GB'] == 1024: base_price += 3500
    elif row['Storage_GB'] == 2048: base_price += 7000

    # GPU
    gpu_add = {
        'Integrated': 0,          'AMD Radeon': 6000,
        'NVIDIA GTX 1650': 10000, 'NVIDIA RTX 3050': 15000,
        'NVIDIA RTX 3060': 22000, 'NVIDIA RTX 3070': 32000,
        'NVIDIA RTX 4060': 28000,
    }
    base_price += gpu_add.get(row['GPU'], 0)

    # Screen size
    if row['Screen_Size'] == 17.3: base_price += 5000
    elif row['Screen_Size'] == 13.3: base_price -= 2000

    # Touchscreen
    base_price += row['Touchscreen'] * 5000

    # Warranty
    base_price += (row['Warranty_Years'] - 1) * 1500

    # Realistic market noise ±4%
    noise = np.random.normal(0, base_price * 0.04)
    return max(round(base_price + noise, -2), 28000)

df['Price_INR'] = df.apply(calculate_price, axis=1)

df.to_csv('data/laptop_data.csv', index=False)
print(f"Dataset created: {len(df)} samples")
print(df[['Brand', 'Processor', 'Generation', 'RAM_GB', 'Price_INR']].head(10))
print(f"Price Range: Rs.{df['Price_INR'].min():,.0f} - Rs.{df['Price_INR'].max():,.0f}")
