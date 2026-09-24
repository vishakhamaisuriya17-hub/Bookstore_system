import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------
st.set_page_config(
    page_title="Bookstore Analytics Dashboard",
    layout="wide"
)

st.title("📚 Bookstore Analytics Dashboard")


# ---------------------------------------------------------
# BOOKSTORE CLASS (same logic as your original script)
# ---------------------------------------------------------
class Bookstore:

    def __init__(self, inventory):
        self.inventory = inventory

    def add_book(self, title, author, genre, price, quantity):
        new_book = {
            "Title": title,
            "Author": author,
            "Genre": genre,
            "Price": price,
            "Quantity": quantity
        }
        self.inventory.loc[len(self.inventory)] = new_book

    def search_book(self, title):
        return self.inventory[
            self.inventory["Title"].str.lower() == title.lower()
        ]

    def update_stock(self, title, quantity_sold):
        index = self.inventory[
            self.inventory["Title"].str.lower() == title.lower()
        ].index

        if len(index) == 0:
            return False, "Book not found!"

        current_quantity = self.inventory.loc[index[0], "Quantity"]

        if quantity_sold > current_quantity:
            return False, "Not enough stock!"

        self.inventory.loc[index[0], "Quantity"] -= quantity_sold
        return True, "Stock updated successfully!"


# ---------------------------------------------------------
# LOAD DATA (file upload, falls back to local CSVs if present)
# ---------------------------------------------------------
st.sidebar.header("Data Source")

inv_file = st.sidebar.file_uploader("Upload inventory.csv", type="csv")
sales_file = st.sidebar.file_uploader("Upload sales.csv", type="csv")

if inv_file is not None:
    inventory_raw = pd.read_csv(inv_file)
elif "inventory" in st.session_state:
    inventory_raw = st.session_state["inventory"]
else:
    try:
        inventory_raw = pd.read_csv("inventory.csv")
    except FileNotFoundError:
        inventory_raw = None

if sales_file is not None:
    sales_raw = pd.read_csv(sales_file)
else:
    try:
        sales_raw = pd.read_csv("sales.csv")
    except FileNotFoundError:
        sales_raw = None

if inventory_raw is None or sales_raw is None:
    st.warning("Upload both inventory.csv and sales.csv from the sidebar to get started.")
    st.stop()

# Keep inventory in session_state so edits (add/update stock) persist across reruns
if "inventory" not in st.session_state:
    st.session_state["inventory"] = inventory_raw.copy()

inventory = st.session_state["inventory"]
store = Bookstore(inventory)

# ---------------------------------------------------------
# PREP SALES DATA
# ---------------------------------------------------------
sales = sales_raw.copy()
sales["Date"] = pd.to_datetime(sales["Date"])

sales = sales.merge(
    inventory[["Title", "Price", "Author", "Genre"]],
    on="Title",
    how="left"
)

quantity = np.array(sales["Quantity Sold"])
price = np.array(sales["Price"])
sales["Total Revenue"] = quantity * price
sales["Month"] = sales["Date"].dt.month_name()

inventory = inventory.drop_duplicates()
sales = sales.drop_duplicates()

# ---------------------------------------------------------
# SIDEBAR NAVIGATION
# ---------------------------------------------------------
page = st.sidebar.radio(
    "Go to",
    ["Overview", "Inventory Management", "Sales Analysis", "Charts", "Final Report"]
)

# ---------------------------------------------------------
# PAGE: OVERVIEW
# ---------------------------------------------------------
if page == "Overview":
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Inventory")
        st.dataframe(inventory, use_container_width=True)

    with col2:
        st.subheader("Sales")
        st.dataframe(sales, use_container_width=True)

    st.subheader("Missing Values")
    c1, c2 = st.columns(2)
    c1.write("**Inventory**")
    c1.write(inventory.isnull().sum())
    c2.write("**Sales**")
    c2.write(sales.isnull().sum())

    st.subheader("Duplicates")
    st.write("Inventory duplicates:", inventory_raw.duplicated().sum())
    st.write("Sales duplicates:", sales_raw.duplicated().sum())

# ---------------------------------------------------------
# PAGE: INVENTORY MANAGEMENT
# ---------------------------------------------------------
elif page == "Inventory Management":
    st.subheader("Search a Book")
    search_title = st.text_input("Book title to search")
    if search_title:
        result = store.search_book(search_title)
        if len(result) > 0:
            st.success("Book found:")
            st.dataframe(result)
        else:
            st.error("Book not found!")

    st.divider()

    st.subheader("Add a New Book")
    with st.form("add_book_form"):
        title = st.text_input("Title")
        author = st.text_input("Author")
        genre = st.text_input("Genre")
        price = st.number_input("Price", min_value=0.0, step=1.0)
        qty = st.number_input("Quantity", min_value=0, step=1)
        submitted = st.form_submit_button("Add Book")

        if submitted:
            if title and author and genre:
                store.add_book(title, author, genre, price, int(qty))
                st.session_state["inventory"] = store.inventory
                st.success("Book added successfully!")
                st.rerun()
            else:
                st.error("Please fill in all fields.")

    st.divider()

    st.subheader("Update Stock (Record a Sale)")
    with st.form("update_stock_form"):
        stock_title = st.text_input("Title of book sold")
        qty_sold = st.number_input("Quantity sold", min_value=0, step=1)
        stock_submitted = st.form_submit_button("Update Stock")

        if stock_submitted:
            ok, message = store.update_stock(stock_title, int(qty_sold))
            st.session_state["inventory"] = store.inventory
            if ok:
                st.success(message)
                st.rerun()
            else:
                st.error(message)

# ---------------------------------------------------------
# PAGE: SALES ANALYSIS
# ---------------------------------------------------------
elif page == "Sales Analysis":
    total_revenue = np.sum(sales["Total Revenue"])
    average_revenue = np.mean(sales["Total Revenue"])
    maximum_revenue = np.max(sales["Total Revenue"])
    minimum_revenue = np.min(sales["Total Revenue"])

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Revenue", f"{total_revenue:,.2f}")
    m2.metric("Average Revenue", f"{average_revenue:,.2f}")
    m3.metric("Max Revenue", f"{maximum_revenue:,.2f}")
    m4.metric("Min Revenue", f"{minimum_revenue:,.2f}")

    genre_sales = sales.groupby("Genre")["Quantity Sold"].sum()
    genre_revenue = sales.groupby("Genre")["Total Revenue"].sum()
    author_sales = sales.groupby("Author")["Quantity Sold"].sum()
    author_revenue = sales.groupby("Author")["Total Revenue"].sum()
    monthly_sales = sales.groupby("Month")["Quantity Sold"].sum()
    monthly_revenue = sales.groupby("Month")["Total Revenue"].sum()
    top_books = sales.groupby("Title")["Quantity Sold"].sum().sort_values(ascending=False)
    top_revenue_books = sales.groupby("Title")["Total Revenue"].sum().sort_values(ascending=False)

    c1, c2 = st.columns(2)
    c1.write("**Genre-wise Sales**")
    c1.dataframe(genre_sales)
    c2.write("**Genre-wise Revenue**")
    c2.dataframe(genre_revenue)

    c3, c4 = st.columns(2)
    c3.write("**Author-wise Sales**")
    c3.dataframe(author_sales)
    c4.write("**Author-wise Revenue**")
    c4.dataframe(author_revenue)

    c5, c6 = st.columns(2)
    c5.write("**Month-wise Sales**")
    c5.dataframe(monthly_sales)
    c6.write("**Month-wise Revenue**")
    c6.dataframe(monthly_revenue)

    st.write("**Top 5 Selling Books**")
    st.dataframe(top_books.head(5))

    st.write("**Top Revenue Books**")
    st.dataframe(top_revenue_books)

# ---------------------------------------------------------
# PAGE: CHARTS
# ---------------------------------------------------------
elif page == "Charts":
    genre_sales = sales.groupby("Genre")["Quantity Sold"].sum()
    author_revenue = sales.groupby("Author")["Total Revenue"].sum()
    monthly_revenue = sales.groupby("Month")["Total Revenue"].sum()
    genre_revenue = sales.groupby("Genre")["Total Revenue"].sum()

    fig1, ax1 = plt.subplots(figsize=(10, 5))
    genre_sales.plot(kind="bar", ax=ax1)
    ax1.set_title("Genre-wise Book Sales")
    ax1.set_xlabel("Genre")
    ax1.set_ylabel("Quantity Sold")
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig1)

    fig2, ax2 = plt.subplots(figsize=(10, 5))
    author_revenue.plot(kind="bar", ax=ax2)
    ax2.set_title("Author-wise Revenue")
    ax2.set_xlabel("Author")
    ax2.set_ylabel("Total Revenue")
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig2)

    fig3, ax3 = plt.subplots(figsize=(10, 5))
    monthly_revenue.plot(kind="line", marker="o", ax=ax3)
    ax3.set_title("Monthly Revenue")
    ax3.set_xlabel("Month")
    ax3.set_ylabel("Revenue")
    plt.xticks(rotation=45)
    ax3.grid(True)
    plt.tight_layout()
    st.pyplot(fig3)

    fig4, ax4 = plt.subplots(figsize=(10, 5))
    sns.barplot(data=sales, x="Genre", y="Total Revenue", ax=ax4)
    ax4.set_title("Revenue by Genre")
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig4)

    fig5, ax5 = plt.subplots(figsize=(8, 8))
    ax5.pie(genre_revenue, labels=genre_revenue.index, autopct="%1.1f%%")
    ax5.set_title("Revenue Distribution by Genre")
    plt.tight_layout()
    st.pyplot(fig5)

    fig6, ax6 = plt.subplots(figsize=(10, 6))
    numeric_data = sales[["Quantity Sold", "Price", "Total Revenue"]]
    correlation = numeric_data.corr()
    sns.heatmap(correlation, annot=True, cmap="coolwarm", linewidths=0.5, fmt=".2f", ax=ax6)
    ax6.set_title("Correlation Heatmap")
    plt.tight_layout()
    st.pyplot(fig6)

# ---------------------------------------------------------
# PAGE: FINAL REPORT
# ---------------------------------------------------------
elif page == "Final Report":
    top_books = sales.groupby("Title")["Quantity Sold"].sum().sort_values(ascending=False)
    top_revenue_books = sales.groupby("Title")["Total Revenue"].sum().sort_values(ascending=False)
    genre_sales = sales.groupby("Genre")["Quantity Sold"].sum()
    author_revenue = sales.groupby("Author")["Total Revenue"].sum()

    st.subheader("📊 Bookstore Final Report")

    st.write("**Total Books in Inventory:**", inventory["Quantity"].sum())
    st.write("**Total Books Sold:**", sales["Quantity Sold"].sum())
    st.write("**Total Revenue:**", sales["Total Revenue"].sum())
    st.write("**Average Revenue:**", sales["Total Revenue"].mean())
    st.write("**Best Selling Book:**", top_books.idxmax())
    st.write("**Highest Revenue Book:**", top_revenue_books.idxmax())
    st.write("**Best Selling Genre:**", genre_sales.idxmax())
    st.write("**Best Revenue Author:**", author_revenue.idxmax())