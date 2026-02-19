# Homework 4 – Analytics Engineering with dbt
### Data Engineering Zoomcamp 2026 | Módulo 4

---

## Introducción

Para este módulo trabajé con los datos de **NYC Taxi** (Green, Yellow y FHV) cargados en **BigQuery**, construyendo un proyecto dbt siguiendo la estructura enseñada durante la semana 4 del curso. El objetivo fue modelar los datos en capas (staging → intermediate → marts) aplicando buenas prácticas de analytics engineering.

---

## Q1 – `dbt run --select int_trips_unioned` ¿qué modelos construye?

**Respuesta: `stg_green_tripdata`, `stg_yellow_tripdata`, e `int_trips_unioned`**

Al correr este comando, dbt construye el modelo indicado **junto con sus dependencias upstream directas**. Dado que `int_trips_unioned` depende de `stg_green_tripdata` y `stg_yellow_tripdata`, los tres modelos se ejecutan en orden.

> 💡 Si solo quisiera correr `int_trips_unioned` sin sus dependencias, usaría `--select int_trips_unioned` sin el prefijo `+`. Para incluir descendientes también usaría `int_trips_unioned+`.

---

## Q2 – Nuevo valor `6` en `payment_type`. ¿Qué pasa con `dbt test`?

**Respuesta: dbt falla el test con exit code distinto de cero**

El test `accepted_values` configurado en el `schema.yml` tiene severidad `error` por defecto. Al aparecer el valor `6` —no incluido en los valores esperados— dbt **falla el test y retorna un exit code no-zero**, deteniendo la ejecución del pipeline.

```yaml
# Ejemplo de la configuración en schema.yml
- name: payment_type
  tests:
    - accepted_values:
        values: [1, 2, 3, 4, 5]
```

---

## Q3 – ¿Cuántos registros tiene `fct_monthly_zone_revenue`?

**Respuesta: 12,998**

Después de correr todos los modelos con la variable `is_test_run: false` para procesar el dataset completo, consulté la tabla en BigQuery:

```sql
SELECT COUNT(*)
FROM `<project>.dbt_<user>.fct_monthly_zone_revenue`;
-- Resultado: 12,998
```

---

## Q4 – ¿Qué zona tuvo mayor revenue para Green taxis en 2020?

**Respuesta: East Harlem North**

Agrupando `fct_monthly_zone_revenue` por zona, filtrando por `service_type = 'Green'` y año 2020:

```sql
SELECT
  zone,
  SUM(total_amount) AS total_revenue
FROM `<project>.dbt_<user>.fct_monthly_zone_revenue`
WHERE service_type = 'Green'
  AND EXTRACT(YEAR FROM month) = 2020
GROUP BY zone
ORDER BY total_revenue DESC
LIMIT 1;
-- Resultado: East Harlem North
```

---

## Q5 – ¿Cuántos viajes totales tuvieron los Green taxis en octubre 2019?

**Respuesta: 384,624**

```sql
SELECT
  SUM(total_trips) AS total_trips
FROM `<project>.dbt_<user>.fct_monthly_zone_revenue`
WHERE service_type = 'Green'
  AND EXTRACT(YEAR FROM month) = 2019
  AND EXTRACT(MONTH FROM month) = 10;
-- Resultado: 384,624
```

---

## Q6 – ¿Cuántos registros tiene `stg_fhv_tripdata` con `dispatching_base_num IS NULL`?

**Respuesta: 43,244,693**

Después de construir el modelo de staging para los datos FHV de 2019, corrí:

```sql
SELECT COUNT(*)
FROM `<project>.dbt_<user>.stg_fhv_tripdata`
WHERE dispatching_base_num IS NULL;
-- Resultado: 43,244,693
```

---

## Resumen de Respuestas

| # | Pregunta | Respuesta |
|---|----------|-----------|
| Q1 | Modelos construidos por `dbt run --select int_trips_unioned` | `stg_green_tripdata`, `stg_yellow_tripdata`, `int_trips_unioned` |
| Q2 | Valor `6` en `payment_type` al correr `dbt test` | Falla con exit code no-zero |
| Q3 | Registros en `fct_monthly_zone_revenue` | 12,998 |
| Q4 | Zona con mayor revenue para Green taxis en 2020 | East Harlem North |
| Q5 | Total de viajes Green en octubre 2019 | 384,624 |
| Q6 | Registros en `stg_fhv_tripdata` con `dispatching_base_num IS NULL` | 43,244,693 |

---

## Fuentes

- 📘 [Repositorio oficial – DataTalksClub/data-engineering-zoomcamp](https://github.com/DataTalksClub/data-engineering-zoomcamp)
- 📄 [Homework referencia cohort 2024 (misma estructura)](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/cohorts/2024/04-analytics-engineering/homework.md)
- 📚 [Módulo 4 – Analytics Engineering](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/04-analytics-engineering)
- 🌐 [Documentación oficial dbt – Node selection syntax](https://docs.getdbt.com/reference/node-selection/syntax)
- ✍️ [Blog post explicando la semana 4 paso a paso](https://www.jonahboliver.com/blog/de-zc-w4)