# Sales Data Analysis Script
# Author: Salman Alhidamkara

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

class SalesAnalyzer:
    def __init__(self, data_path=None):
        self.data = None
        if data_path:
            self.load_data(data_path)
    
    def load_data(self, data_path):
        """Load data dari file CSV"""
        try:
            self.data = pd.read_csv(data_path)
            print(f"Data loaded: {len(self.data)} rows, {len(self.data.columns)} columns")
            return True
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
    
    def generate_sample_data(self):
        """Generate sample data untuk demo"""
        np.random.seed(42)
        dates = pd.date_range('2024-01-01', '2024-12-31', freq='D')
        
        products = ['Product A', 'Product B', 'Product C', 'Product D']
        categories = ['Electronics', 'Fashion', 'Food', 'Home']
        
        data = []
        for date in dates:
            for product in products:
                sales = np.random.randint(1, 100)
                price = np.random.randint(50000, 500000)
                category = np.random.choice(categories)
                data.append({
                    'date': date,
                    'product': product,
                    'category': category,
                    'sales': sales,
                    'price': price,
                    'revenue': sales * price
                })
        
        self.data = pd.DataFrame(data)
        print(f"Sample data generated: {len(self.data)} rows")
        return self.data
    
    def clean_data(self):
        """Bersihkan data"""
        if self.data is None:
            print("No data loaded")
            return
        
        # Cek missing values
        print(f"Missing values: {self.data.isnull().sum().sum()}")
        self.data = self.data.dropna()
        
        # Convert date
        self.data['date'] = pd.to_datetime(self.data['date'])
        
        # Remove duplicates
        self.data = self.data.drop_duplicates()
        
        print("Data cleaned successfully")
    
    def analyze_sales_trend(self):
        """Analisis tren penjualan"""
        if self.data is None:
            print("No data loaded")
            return
        
        # Sales by month
        self.data['month'] = self.data['date'].dt.to_period('M')
        monthly_sales = self.data.groupby('month')['sales'].sum()
        
        # Plot
        plt.figure(figsize=(12, 6))
        monthly_sales.plot(kind='line', marker='o', color='green')
        plt.title('Monthly Sales Trend', fontsize=14)
        plt.xlabel('Month')
        plt.ylabel('Total Sales')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        plt.savefig('monthly_sales_trend.png')
        plt.show()
        
        return monthly_sales
    
    def analyze_top_products(self):
        """Identifikasi produk terlaris"""
        if self.data is None:
            print("No data loaded")
            return
        
        top_products = self.data.groupby('product')['sales'].sum().sort_values(ascending=False)
        
        plt.figure(figsize=(10, 6))
        top_products.head(10).plot(kind='bar', color='skyblue')
        plt.title('Top 10 Best Selling Products', fontsize=14)
        plt.xlabel('Product')
        plt.ylabel('Total Sales')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.savefig('top_products.png')
        plt.show()
        
        return top_products
    
    def analyze_category_performance(self):
        """Analisis performa per kategori"""
        if self.data is None:
            print("No data loaded")
            return
        
        category_sales = self.data.groupby('category')['sales'].sum()
        category_revenue = self.data.groupby('category')['revenue'].sum()
        
        fig, axes = plt.subplots(1, 2, figsize=(14, 6))
        
        category_sales.plot(kind='pie', autopct='%1.1f%%', ax=axes[0])
        axes[0].set_title('Sales Distribution by Category')
        axes[0].set_ylabel('')
        
        category_revenue.plot(kind='bar', ax=axes[1], color='coral')
        axes[1].set_title('Revenue by Category')
        axes[1].set_xlabel('Category')
        axes[1].set_ylabel('Revenue')
        
        plt.tight_layout()
        plt.savefig('category_analysis.png')
        plt.show()
        
        return category_sales, category_revenue
    
    def generate_report(self):
        """Generate laporan analisis"""
        if self.data is None:
            print("No data loaded")
            return
        
        total_revenue = self.data['revenue'].sum()
        total_sales = self.data['sales'].sum()
        avg_price = self.data['price'].mean()
        
        report = f"""
SALES DATA ANALYSIS REPORT
==========================
Analysis Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

SUMMARY STATISTICS:
- Total Revenue: Rp {total_revenue:,.0f}
- Total Sales: {total_sales:,.0f} units
- Average Price: Rp {avg_price:,.0f}
- Total Transactions: {len(self.data):,}

TOP 3 PRODUCTS:
{self.analyze_top_products().head(3).to_string()}

MONTH WITH HIGHEST SALES:
{self.analyze_sales_trend().idxmax()} - {self.analyze_sales_trend().max():,.0f} units

RECOMMENDATIONS:
1. Focus marketing on top performing products
2. Consider bundling slow-moving products with best sellers
3. Increase inventory before peak months
"""
        print(report)
        
        # Save report
        with open('sales_analysis_report.txt', 'w') as f:
            f.write(report)
        
        print("Report saved to sales_analysis_report.txt")

def main():
    analyzer = SalesAnalyzer()
    
    print("Sales Data Analysis Tool")
    print("-" * 40)
    print("1. Use sample data (demo)")
    print("2. Load from CSV file")
    
    choice = input("Pilih (1/2): ")
    
    if choice == "1":
        analyzer.generate_sample_data()
    else:
        csv_path = input("Path ke file CSV: ")
        analyzer.load_data(csv_path)
    
    if analyzer.data is not None:
        analyzer.clean_data()
        analyzer.analyze_sales_trend()
        analyzer.analyze_top_products()
        analyzer.analyze_category_performance()
        analyzer.generate_report()

if __name__ == "__main__":
    main()
