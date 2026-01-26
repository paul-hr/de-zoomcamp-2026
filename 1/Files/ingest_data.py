import pandas as pd
from sqlalchemy import create_engine

# 1. Configurar la conexión
# Nota el puerto 5433, que es el que definiste en tu docker-compose
engine = create_engine('postgresql://postgres:postgres@localhost:5433/ny_taxi')

print("Conectando a la base de datos...")

# 2. Cargar y subir los datos de ZONAS (CSV)
print("Leyendo zonas...")
df_zones = pd.read_csv('taxi_zone_lookup.csv')
df_zones.to_sql(name='zones', con=engine, if_exists='replace', index=False)
print("--> Zonas cargadas exitosamente.")

# 3. Cargar y subir los datos de VIAJES (Parquet)
print("Leyendo datos de viajes (esto puede tardar un poco)...")
df_trips = pd.read_parquet('green_tripdata_2025-11.parquet')

# Opcional: Asegurar que las fechas sean datetime (pandas suele hacerlo auto con parquet, pero por seguridad)
df_trips['lpep_pickup_datetime'] = pd.to_datetime(df_trips['lpep_pickup_datetime'])
df_trips['lpep_dropoff_datetime'] = pd.to_datetime(df_trips['lpep_dropoff_datetime'])

# Subir a la base de datos
# 'chunksize' ayuda a que no se congele si el archivo es muy grande
df_trips.to_sql(name='green_taxi_trips', con=engine, if_exists='replace', index=False, chunksize=100000)
print("--> Viajes cargados exitosamente.")