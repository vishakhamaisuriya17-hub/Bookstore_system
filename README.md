# 📚 Bookstore Management System

A Python-based **Bookstore Inventory & Sales Management System** that combines an object-oriented inventory manager with data analysis and visualization of sales performance using **Pandas**, **NumPy**, **Matplotlib**, and **Seaborn**.

---

## 📌 Overview

This project simulates the day-to-day operations of a bookstore — managing inventory, tracking sales, and generating business insights. It reads inventory and sales data from CSV files, performs data cleaning, and produces detailed analytics and visual reports to help understand sales trends, top-performing books, authors, and genres.

---

## ✨ Features

### 🏪 Inventory Management (OOP)
- Display current book inventory
- Add new books to inventory
- Search for a book by title
- Update stock after a sale (with insufficient stock handling)

### 🧹 Data Cleaning
- Detects and reports missing values in inventory and sales data
- Detects and removes duplicate records

### 📊 Sales Analysis
- Total, average, maximum, and minimum revenue calculations (NumPy)
- Genre-wise sales and revenue breakdown
- Author-wise sales and revenue breakdown
- Month-wise sales and revenue trends
- Top-selling books and top revenue-generating books

### 📈 Data Visualization
- Genre-wise sales bar chart
- Author-wise revenue bar chart
- Monthly revenue trend line chart
- Revenue by genre (Seaborn bar plot)
- Revenue distribution pie chart
- Correlation heatmap (Quantity Sold, Price, Total Revenue)

### 📑 Final Business Report
- Total books in inventory
- Total books sold
- Total and average revenue
- Best-selling book
- Highest revenue-generating book
- Best-selling genre
- Top revenue-generating author

---

## 🗂️ Project Structure

```
exam/
│
├── Bookstore_system.py     # Main Python script (core logic)
├── inventory.csv           # Book inventory data
├── sales.csv                # Sales transaction data
└── README.md                # Project documentation
```

---

## 🛠️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python 3.x | Core programming language |
| Pandas | Data manipulation & analysis |
| NumPy | Numerical computations |
| Matplotlib | Data visualization |
| Seaborn | Statistical data visualization |

---

## ⚙️ Installation & Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/vishakhamaisuriya17-hub/Bookstore_system.git
   cd Bookstore_system
   ```

2. **Install the required dependencies**
   ```bash
   pip install pandas numpy matplotlib seaborn
   ```

3. **Ensure the CSV files are present**
   Make sure `inventory.csv` and `sales.csv` are in the same directory as the script.

4. **Run the script**
   ```bash
   python Bookstore_system.py
   ```

---

## 📄 Data Format

### `inventory.csv`
| Column | Description |
|--------|--------------|
| Title | Book title |
| Author | Book author |
| Genre | Book genre |
| Price | Price per unit |
| Quantity | Stock quantity |

### `sales.csv`
| Column | Description |
|--------|--------------|
| Date | Date of sale |
| Title | Book title sold |
| Quantity Sold | Number of units sold |

---

## 📷 Sample Output

Running the script prints:
- Full inventory and sales tables
- Missing value & duplicate reports
- Revenue statistics
- Genre/author/month-wise breakdowns
- Top-selling and top-revenue books

...and displays 6 charts covering sales and revenue trends across genres, authors, and time.

---

## 🚀 Future Improvements

- Add a command-line or GUI interface for interactive use
- Export analysis results and charts to PDF/Excel reports
- Add persistent storage (database) instead of CSV files
- Include unit tests for the `Bookstore` class methods

---

## 👩‍💻 Author

**Vishakha Maisuriya**
🔗 [GitHub Repository](https://github.com/vishakhamaisuriya17-hub/Bookstore_system.git)

---

## 📃 License

This project is open-source and available for educational purposes.
