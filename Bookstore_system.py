import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

inventory = pd.read_csv("inventory.csv")
sales = pd.read_csv("sales.csv")


print("Inventory:")
print(inventory)

print("Sales:")
print(sales)

class Bookstore:

    def __init__(self, inventory):
        self.inventory = inventory

    def display_inventory(self):
        print("\nBOOK INVENTORY")
        print(self.inventory)

    def add_book(self, title, author, genre, price, quantity):
        new_book = {
            "Title": title,
            "Author": author,
            "Genre": genre,
            "Price": price,
            "Quantity": quantity
        }

        self.inventory.loc[len(self.inventory)] = new_book
        print("\nBook added successfully!")

    def search_book(self, title):
        result = self.inventory[
            self.inventory["Title"].str.lower() == title.lower()
        ]

        if len(result) > 0:
            print("\nBook Found:")
            print(result)
        else:
            print("\nBook not found!")

    def update_stock(self, title, quantity_sold):
        index = self.inventory[
            self.inventory["Title"].str.lower() == title.lower()
        ].index

        if len(index) > 0:
            current_quantity = self.inventory.loc[index[0], "Quantity"]

            if quantity_sold <= current_quantity:
                self.inventory.loc[index[0], "Quantity"] -= quantity_sold
                print("\nStock updated successfully!")
            else:
                print("\nNot enough stock!")
        else:
            print("\nBook not found!")

sales["Date"] = pd.to_datetime(sales["Date"])

sales = sales.merge(
    inventory[["Title", "Price", "Author", "Genre"]],
    on="Title",
    how="left"
)

quantity = np.array(sales["Quantity Sold"])
price = np.array(sales["Price"])

revenue = quantity * price

sales["Total Revenue"] = revenue

store = Bookstore(inventory)

store.display_inventory()

store.search_book("Python Basics")

store.add_book(
    "Python for Beginners",
    "Michael Lee",
    "Programming",
    550,
    25
)

store.update_stock(
    "Python Basics",
    2
)

print("\nMISSING VALUES")

print("\nInventory:")
print(inventory.isnull().sum())

print("\nSales:")
print(sales.isnull().sum())

print("\nDUPLICATES")

print(
    "Inventory duplicates:",
    inventory.duplicated().sum()
)

print(
    "Sales duplicates:",
    sales.duplicated().sum()
)

inventory = inventory.drop_duplicates()

sales = sales.drop_duplicates()

total_revenue = np.sum(revenue)

average_revenue = np.mean(revenue)

maximum_revenue = np.max(revenue)

minimum_revenue = np.min(revenue)

print("\nNUMPY CALCULATIONS")

print("Total Revenue:", total_revenue)

print("Average Revenue:", average_revenue)

print("Maximum Revenue:", maximum_revenue)

print("Minimum Revenue:", minimum_revenue)

genre_sales = sales.groupby(
    "Genre"
)["Quantity Sold"].sum()

print("\nGENRE-WISE SALES")
print(genre_sales)

genre_revenue = sales.groupby(
    "Genre"
)["Total Revenue"].sum()

print("\nGENRE-WISE REVENUE")
print(genre_revenue)

author_sales = sales.groupby(
    "Author"
)["Quantity Sold"].sum()

print("\nAUTHOR-WISE SALES")
print(author_sales)

author_revenue = sales.groupby(
    "Author"
)["Total Revenue"].sum()

print("\nAUTHOR-WISE REVENUE")
print(author_revenue)

sales["Month"] = sales["Date"].dt.month_name()

monthly_sales = sales.groupby(
    "Month"
)["Quantity Sold"].sum()

print("\nMONTH-WISE SALES")
print(monthly_sales)

monthly_revenue = sales.groupby(
    "Month"
)["Total Revenue"].sum()

print("\nMONTH-WISE REVENUE")
print(monthly_revenue)

top_books = sales.groupby(
    "Title"
)["Quantity Sold"].sum()

top_books = top_books.sort_values(
    ascending=False
)

print("\nTOP SELLING BOOKS")
print(top_books)

print("\nTOP 5 BOOKS")
print(top_books.head(5))

top_revenue_books = sales.groupby(
    "Title"
)["Total Revenue"].sum()

top_revenue_books = top_revenue_books.sort_values(
    ascending=False
)

print( "\nTOP REVENUE BOOKS")
print(top_revenue_books)

plt.figure(figsize=(10, 5))

genre_sales.plot(
    kind="bar"
)

plt.title("Genre-wise Book Sales")
plt.xlabel("Genre")
plt.ylabel("Quantity Sold")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 5))

author_revenue.plot(
    kind="bar"
)

plt.title("Author-wise Revenue")
plt.xlabel("Author")
plt.ylabel("Total Revenue")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 5))

monthly_revenue.plot(
    kind="line",
    marker="o"
)

plt.title("Monthly Revenue")
plt.xlabel("Month")
plt.ylabel("Revenue")
plt.xticks(rotation=45)
plt.grid(True)
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 5))

sns.barplot(
    data=sales,
    x="Genre",
    y="Total Revenue"
)

plt.title("Revenue by Genre")
plt.xlabel("Genre")
plt.ylabel("Total Revenue")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 5))

plt.pie(
    genre_revenue,
    labels=genre_revenue.index,
    autopct="%1.1f%%"
    )
plt.title("Revenue Distribution by Genre")
plt.tight_layout()
plt.show()

plt.figure(figsize=(10, 6))

numeric_data = sales[
    ["Quantity Sold", "Price", "Total Revenue"]
]

correlation = numeric_data.corr()

sns.heatmap(
    correlation,
    annot=True,
    cmap="coolwarm",
    linewidths=0.5,
    fmt=".2f"
)

plt.title("Correlation Heatmap")
plt.tight_layout()
plt.show()

print("\n")

print("BOOKSTORE FINAL REPORT")


print(
    "\nTotal Books in Inventory:",
    inventory["Quantity"].sum()
)

print(
    "Total Books Sold:",
    sales["Quantity Sold"].sum()
)

print(
    "Total Revenue:",
    sales["Total Revenue"].sum()
)

print(
    "Average Revenue:",
    sales["Total Revenue"].mean()
)

print(
    "Best Selling Book:",
    top_books.idxmax()
)

print(
    "Highest Revenue Book:",
    top_revenue_books.idxmax()
)

print(
    "Best Selling Genre:",
    genre_sales.idxmax()
)

print(
    "Best Revenue Author:",
    author_revenue.idxmax()
)
