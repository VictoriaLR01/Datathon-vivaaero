import os
import sys
import pandas as pd
import numpy as np

flights = pd.read_csv(sys.argv[1])
sales = pd.read_csv(sys.argv[2])

flights.drop_duplicates(subset='Flight_ID', keep='first', inplace=True)

# Convertir las cadenas a datetime
flights['STD'] = pd.to_datetime(flights['STD'])
flights['STA'] = pd.to_datetime(flights['STA'])

# Calcular la duración en horas y crear una columna para ello
flights['Duration'] = (flights['STA'] - flights['STD']).dt.total_seconds() / 3600

# Extraer la hora del día de cada salida
flights['Hour of Day'] = flights['STD'].dt.hour

flights['Passengers'] = np.where(flights['Passengers'] > flights['Capacity'], flights['Capacity'], flights['Passengers'])
flights['Bookings'] = np.where(flights['Bookings'] > flights['Capacity'], flights['Capacity'], flights['Bookings'])

flights['Ocupancia'] = flights['Passengers'] / flights['Capacity']

flights['Passengers'] = flights['Passengers'].fillna(-1).astype(int)
flights['Bookings'] = flights['Bookings'].fillna(-1).astype(int)

flights_Test = flights[flights['STD'] > '2023-12-31']

flights_Test['Passengers'] = np.nan
flights_Test['Bookings'] = np.nan

flights_Test.to_csv(r"C:\Users\jdami\OneDrive\Documents\GitHub\Datathon-vivaaero\pred\Filghts_pred.csv", index=False)


sales = sales[sales.ProductType.isin(['Botanas', 'Licores','Galletas','Bebidas Calientes', 'Perecederos', 'Refrescos', 'Sopas', 'Lacteos'])]
sales = sales[~sales['ProductName'].isin(['Combo Stl', 'Maxi Combo'])]
sales[sales.Flight_ID.isin(flights_Test.Flight_ID)].drop(columns='TotalSales').to_csv(r"C:\Users\jdami\OneDrive\Documents\GitHub\Datathon-vivaaero\pred\Sales_pred.csv", index=False)

flights = flights[flights['STD'] <= '2023-12-31']
flights.dropna(subset=['Aeronave'], inplace=True)

flights.to_csv(r"C:\Users\jdami\OneDrive\Documents\GitHub\Datathon-vivaaero\train_test\Filghts_train_test.csv", index=False)

sales = sales[~sales.Flight_ID.isin(flights_Test.Flight_ID)]
sales.to_csv(r"C:\Users\jdami\OneDrive\Documents\GitHub\Datathon-vivaaero\train_test\Sales_train_test.csv", index=False)