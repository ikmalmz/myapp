import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

st.title('Hello, Dicoding Team!')
st.write('Selamat datang di dashboard pertama Saya! I am Muhammad Ikmal Muqtafi Zulfa, Hope you can understand my data analysis!:))')


#Melakukan Load datasets
orders_dataset_df = pd.read_csv(r'D:\submission\Dashboard\orders_dataset.csv')
order_reviews_dataset_df = pd.read_csv(r'D:\submission\Dashboard\order_reviews_dataset.csv')
merged_orders_items = pd.read_csv(r'D:\submission\Dashboard\merged_orders_items.csv')
merged_payment_product = pd.read_csv(r'D:\submission\Dashboard\merged_payment_product.csv')

#Membuat Title dari dashboard
st.title('Dashboard Analisis Data : E-Commerce Public Dataset')

#Pertanyaan 1: Bagaimana tingkat kepuasan pelanggan terhadap pengiriman?
st.header('Tingkat Kepuasan Pelanggan terhadap Pengiriman')

import pandas as pd

#Memastikan kolom bertipe datetime
orders_dataset_df['order_delivered_customer_date'] = pd.to_datetime(orders_dataset_df['order_delivered_customer_date'])
orders_dataset_df['order_purchase_timestamp'] = pd.to_datetime(orders_dataset_df['order_purchase_timestamp'])

#Menghitung order_delivery_time dalam hari
orders_dataset_df['order_delivery_time'] = (orders_dataset_df['order_delivered_customer_date'] -
                                            orders_dataset_df['order_purchase_timestamp']).dt.days

def delivery_time_category(delivery_time):
    if delivery_time <= 7:
        return 'Fast'
    elif delivery_time <= 14:
        return 'Medium'
    else:
        return 'Slow'

orders_dataset_df['delivery_time_category'] = orders_dataset_df['order_delivery_time'].apply(delivery_time_category)

merged_orders_items['order_value'] = merged_orders_items['price'] + merged_orders_items['freight_value']
merged_orders_items['shipping_cost_percentage'] = (merged_orders_items['freight_value'] /
                                                 merged_orders_items['order_value']) * 100






# Distribusi Waktu Pengiriman
st.subheader('Distribusi Waktu Pengiriman')
fig, ax = plt.subplots()
ax.hist(orders_dataset_df['order_delivery_time'], bins=20)
ax.set_xlabel('Waktu Pengiriman (hari)')
ax.set_ylabel('Jumlah Pesanan')
ax.set_title('Distribusi Waktu Pengiriman')
st.pyplot(fig)

# Boxplot Waktu Pengiriman Berdasarkan Kategori
st.subheader('Boxplot Waktu Pengiriman Berdasarkan Kategori')
fig, ax = plt.subplots()
sns.boxplot(x='delivery_time_category', y='order_delivery_time', data=orders_dataset_df, ax=ax)
ax.set_xlabel('Kategori Waktu Pengiriman')
ax.set_ylabel('Waktu Pengiriman (hari)')
ax.set_title('Boxplot Waktu Pengiriman Berdasarkan Kategori')
st.pyplot(fig)

# Hubungan antara Waktu Pengiriman dan Skor Review
st.subheader('Hubungan antara Waktu Pengiriman dan Skor Review')
combined_df = orders_dataset_df.merge(order_reviews_dataset_df, on='order_id')
fig, ax = plt.subplots()
ax.scatter(combined_df['order_delivery_time'], combined_df['review_score'])
ax.set_xlabel('Waktu Pengiriman (hari)')
ax.set_ylabel('Skor Review')
ax.set_title('Hubungan antara Waktu Pengiriman dan Skor Review')
st.pyplot(fig)

correlation = combined_df['order_delivery_time'].corr(combined_df['review_score'])
st.write(f'Korelasi antara Waktu Pengiriman dan Skor Review: {correlation}')

# Pengaruh Biaya Pengiriman terhadap Kepuasan
st.subheader('Pengaruh Biaya Pengiriman terhadap Kepuasan')
combined_df = merged_orders_items.merge(order_reviews_dataset_df, on='order_id', how='inner')
fig, ax = plt.subplots()
ax.scatter(combined_df['shipping_cost_percentage'], combined_df['review_score'])
ax.set_xlabel('Persentase Biaya Pengiriman')
ax.set_ylabel('Skor Review')
ax.set_title('Hubungan antara Persentase Biaya Pengiriman dan Skor Review')
st.pyplot(fig)

# Pertanyaan 2: Bagaimana distribusi jumlah pembayaran menurut kategori produk?
st.header('Distribusi Jumlah Pembayaran menurut Kategori Produk')

# Distribusi Jumlah Pembayaran per Kategori Produk
st.subheader('Distribusi Jumlah Pembayaran per Kategori Produk')
payment_per_category = merged_payment_product.groupby('product_category_name')['payment_value'].sum()
fig, ax = plt.subplots()
payment_per_category.plot(kind='barh', ax=ax, figsize=(20, 15))
ax.set_xlabel('Total Pembayaran')
ax.set_ylabel('Kategori Produk')
ax.set_title('Total Pembayaran per Kategori Produk')
st.pyplot(fig)

# Hubungan antara Kategori Produk dan Metode Pembayaran
st.subheader('Hubungan antara Kategori Produk dan Metode Pembayaran')
payment_method_per_category = pd.crosstab(merged_payment_product['product_category_name'],
                                          merged_payment_product['payment_type'])
st.write(payment_method_per_category)

