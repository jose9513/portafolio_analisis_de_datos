Caso de Negocio: Auditoria de Rentabilidad por Volumen
El Problema: La empresa necesitaba identificar que material de joyeria genera el mayor margen de ganancia neta, aislando unicamente a los clientes que compran por volumen. La solucion: Desarrollé un script en MySQL que:
    . Filtra compras unitarias (WHERE cantidad > 1).
    . Agrupa el inventario por tipo de material (GROUP BY).
    . Calcula la ganancia neta real [(Precio Venta - costo) * Cantidad].
    . Excluye del reporte lineas de negocio con ganancias inferiores a $10,000 usando la cláucula (HAVING).

El insight (Toma de Decisiones): El analisis reveló que el Acero 316L es el producto estrella para ventas B2B, superando a la Plata 925 y sugiriendo una reasignación del presupuesto de importación.
