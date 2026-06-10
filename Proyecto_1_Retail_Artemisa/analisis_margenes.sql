SELECT Material, SUM((Precio_Venta - Costo_Adquisicion) * Cantidad) As Ganancia_Total
FROM Ventas_joyeria_fake
WHERE cantidad > 1
GROUP BY Material
Having SUM((Precio_Venta - Costo_Adquisicion) * Cantidad) > 10000