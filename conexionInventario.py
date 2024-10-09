#import sqilte3

import mysql.connector  #pip install mysql-connector-python

class ComunicacionInventario():

    def __init__(self):
        self.conexion = mysql.connector.connect(host='127.0.0.1',
                                                port="3306",
                                                database ='celtics12', 
                                                user = 'root',
                                                password ='Ca22021956*')
    
    
    #CODIFICACION DE INVENTARIOS-----------------------------------------------------------------------------------------------------#
    def inserta_datos_empresa(self,Razon_social,rif,direccion_fiscal,titulo1,titulo2,titulo3,titulo4):
        cur = self.conexion.cursor()
        sql='''INSERT INTO datos_empresas (Razon_social,rif,direccion_fiscal,titulo1,titulo2,titulo3,titulo4) VALUES (%s,%s,%s,%s,%s,%s,%s)'''
        val = (Razon_social,rif,direccion_fiscal,titulo1,titulo2,titulo3,titulo4)
        cur.execute(sql,val)
        self.conexion.commit()    
        cur.close()

    def elimina_datos_empresa(self,Razon_social1):
        cur = self.conexion.cursor()
        sql='''DELETE FROM datos_empresas WHERE Razon_social= '{}' '''.format(Razon_social1)
        cur.execute(sql)
        nom = cur.rowcount
        self.conexion.commit()    
        cur.close()
        return nom


    def inserta_codificacion_inventario(self,codigo,Producto):
        cur = self.conexion.cursor()
        sql='''INSERT INTO base_datos (codigo,Producto) VALUES (%s,%s)'''
        val = (codigo,Producto)
        cur.execute(sql,val)
        self.conexion.commit()    
        cur.close()

    def mostrar_datos_de_la_empresa(self):
        cur = self.conexion.cursor()
        sql='''SELECT * FROM datos_empresas'''
        cur.execute(sql)
        datos = cur.fetchall()
        return datos

    def mostrar_codificacion(self):
        cur = self.conexion.cursor()
        sql='''SELECT * FROM base_datos'''
        cur.execute(sql)
        datos = cur.fetchall()
        return datos

    def mostrar_codificacion2(self):
        cur = self.conexion.cursor()
        sql='''SELECT * FROM base_datos'''
        cur.execute(sql)
        datos = cur.fetchall()
        return datos


    def elimina_codificacion(self,codigo):
        cur = self.conexion.cursor()
        sql='''DELETE FROM base_datos WHERE codigo= '{}' '''.format(codigo)
        cur.execute(sql)
        nom = cur.rowcount
        self.conexion.commit()    
        cur.close()
        return nom

    def mostras_compras(self,NFactura):
        cur = self.conexion.cursor()
        #sql="SELECT NFactura,Nlote,Fecha,Proveedor,codigo,Producto,Cantidades,CU,(Cantidades)*(CU) FROM compras1"
        sql = "SELECT * FROM compras1 as C WHERE C.NFactura="+NFactura
        cur.execute(sql)
        datos = cur.fetchall() 
        return datos


    def mostras_compras1(self):
        cur = self.conexion.cursor()
        sql="SELECT * FROM compras1"
        cur.execute(sql)
        datos = cur.fetchall() 
        return datos


    def elimina_item_modulo_de_compra(self,NFactura):
        cur = self.conexion.cursor()
        sql='''DELETE FROM compras1 WHERE NFactura= '{}' '''.format(NFactura)
        cur.execute(sql)
        nom = cur.rowcount
        self.conexion.commit()    
        cur.close()
        return nom

    def mostras_salidas(self,NFactura):
        cur = self.conexion.cursor()
        sql="SELECT * FROM salidas1 as S WHERE S.NFactura="+NFactura
        cur.execute(sql)
        datos = cur.fetchall()
        return datos

    def mostras_salidas1(self):
        cur = self.conexion.cursor()
        sql="SELECT * FROM salidas1"
        cur.execute(sql)
        datos = cur.fetchall() 
        return datos

    def elimina_item_modulo_de_salida(self,NFactura):
        cur = self.conexion.cursor()
        sql='''DELETE FROM salidas1 WHERE NFactura= '{}' '''.format(NFactura)
        cur.execute(sql)
        nom = cur.rowcount
        self.conexion.commit()    
        cur.close()
        return nom


    def insertar_compras(self,NFactura,Nlote,Fecha,Proveedor,codigo,Producto,Cantidades,CU):
        cur = self.conexion.cursor()
        sql='''INSERT INTO compras1 (NFactura,Nlote,Fecha,Proveedor,codigo,Producto,Cantidades,CU) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'''
        val = (NFactura,Nlote,Fecha,Proveedor,codigo,Producto,Cantidades,CU)
        cur.execute(sql,val)
        self.conexion.commit()    
        cur.close()
        

    def insertar_salidas(self,NFactura,Nlote,Fecha,cliente,codigo,Producto,Cantidades,CU):
        cur = self.conexion.cursor()
        sql='''INSERT INTO salidas1 (NFactura,Nlote,Fecha,cliente,codigo,Producto,Cantidades,CU) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'''
        val = (NFactura,Nlote,Fecha,cliente,codigo,Producto,Cantidades,CU)
        cur.execute(sql,val)
        self.conexion.commit()    
        cur.close()

    def valoracion(self,val1,val2,val3): 
        cur = self.conexion.cursor()
        sql = '''SELECT ((SUM((inv.Cantidades)*(inv.CU)) + (                  
                        SELECT SUM((C.Cantidades)*(C.CU)) FROM compras1 AS C WHERE C.codigo =%s))
                        / (SELECT(SUM((inv.Cantidades) + (                  
                            SELECT SUM((C.Cantidades)) FROM compras1 AS C WHERE C.codigo =%s)
                            )))) as Inventario_Final                            
                FROM inv_inicial AS inv 
                WHERE inv.codigo =%s
            '''
        val1 = val1[0]
        val2 = val2[0]
        val3 = val3[0]
        cur.execute(sql,(val1,val2,val3))
        table_rows = cur.fetchall()
        cur.close()     
        return table_rows


    def reportes_all_inventario(self): 
        cur = self.conexion.cursor()
        sql = '''SELECT  
                    I.codigo,                                                                               
                    I.Producto,                                                                                     
                    I.Cantidades_iniciales,                                     
                    I.CU_iniciales,                                     
                    I.Total_iniciales,
                    C.Cantidades1,                                                                                      
                    C.CU_Compras,                                       
                    C.Total1,
                    S.Cantidades2,
                    W.CU_Salidas,
                    P.Total2,
                    A.Cantidades3,
                    A.CU3,       
                    A.Total3 
                    FROM (SELECT inv.codigo,                                                                                
                                 inv.Producto,                                                      
                                 SUM(inv.Cantidades) AS Cantidades_iniciales,                                                       
                                 AVG(inv.CU) AS CU_iniciales,                                                                           
                                 SUM(inv.Cantidades) * AVG(inv.CU) AS Total_iniciales                                                                           
                                 FROM inv_inicial AS inv                                                            
                                 GROUP BY inv.codigo, inv.Producto                                                      
                    ) I
                    RIGHT JOIN (SELECT C.codigo,                                                                                
                                       C.Producto,                                                     
                                       SUM(C.Cantidades) AS Cantidades1,                                                
                                       AVG(C.CU) AS CU_Compras,         
                                       SUM(C.Cantidades) *  AVG(C.CU) AS Total1                                                                      
                                FROM compras1 AS C                                                       
                                GROUP BY C.codigo,C.Producto
                    ) C ON C.codigo = I.codigo
                    RIGHT JOIN (SELECT S.codigo,                                                                          
                                       SUM(S.Cantidades) AS Cantidades2
                                FROM salidas1 AS S                                          
                                GROUP BY S.codigo                                                               
                    ) S ON C.codigo = S.codigo
                    RIGHT JOIN (SELECT inv.codigo,
                                       ((SUM((inv.Cantidades)*(inv.CU)) + (                  
                                       SELECT SUM((C.Cantidades)*(C.CU)) FROM compras1 AS C WHERE inv.codigo = C.codigo))
                                        / (SELECT(SUM((inv.Cantidades) + (                  
                                        SELECT SUM((C.Cantidades)) FROM compras1 AS C WHERE inv.codigo = C.codigo))))) as CU_Salidas
                                FROM inv_inicial as inv                 
                                GROUP BY inv.codigo                                                     
                    ) W ON C.codigo = W.codigo
                    RIGHT JOIN (SELECT inv.codigo,
                                        ((SUM(inv.Cantidades)*(inv.CU)) +( 
                                        SUM(0) +(
                                        SELECT SUM((C.Cantidades)*(C.CU)) FROM compras1 AS C 
                                        WHERE inv.codigo = C.codigo))) / (
                                        (SUM(inv.Cantidades)) +(
                                        (SUM(0) +(
                                        SELECT SUM(C.Cantidades) FROM compras1 AS C
                                        WHERE inv.codigo = C.codigo))))  *(
                                        SUM(0) + (
                                        SELECT SUM(S.Cantidades) FROM salidas1 AS S
                                        WHERE inv.codigo = S.codigo)) as Total2
                                FROM inv_inicial as inv                                      
                                GROUP BY inv.codigo,inv.CU                               
                    ) P ON S.codigo = P.codigo
                    RIGHT JOIN (SELECT  inv.codigo,
                                        (SUM(inv.Cantidades) +( 
                                        SELECT SUM(vc.Cantidades) FROM compras1 AS vc 
                                        WHERE inv.codigo =vc.codigo)-(
                                        SELECT SUM(S.Cantidades) FROM salidas1 AS S                                 
                                        WHERE inv.codigo =S.codigo)) AS Cantidades3,
                                        #---------------------------------------------------------------#
                                        ((SUM(inv.Cantidades)*(inv.CU)) +(
                                        (SUM(0))) + (
                                        SELECT (SUM(C.Cantidades))*(AVG(C.CU)) FROM compras1 AS C
                                        WHERE inv.codigo = C.codigo) - (
                                        ((SUM(inv.Cantidades)*(inv.CU)) +( 
                                        SUM(0) +(
                                        SELECT SUM((C.Cantidades)*(C.CU)) FROM compras1 AS C 
                                        WHERE inv.codigo = C.codigo))) / (
                                        (SUM(inv.Cantidades)) +(
                                        (SUM(0) +(
                                        SELECT SUM(C.Cantidades) FROM compras1 AS C
                                        WHERE inv.codigo = C.codigo))))  *(
                                        SUM(0) + (
                                        SELECT SUM(S.Cantidades) FROM salidas1 AS S
                                        WHERE inv.codigo = S.codigo)))) / (
                                         (SUM(inv.Cantidades) +( 
                                        SELECT SUM(vc.Cantidades) FROM compras1 AS vc 
                                        WHERE inv.codigo =vc.codigo)-(
                                        SELECT SUM(S.Cantidades) FROM salidas1 AS S                                 
                                        WHERE inv.codigo =S.codigo)))AS CU3,
                                        #---------------------------------------------------------------#
                                        (SUM(inv.Cantidades)*(inv.CU)) +(
                                        (SUM(0))) + (
                                        SELECT (SUM(C.Cantidades))*(AVG(C.CU)) FROM compras1 AS C
                                        WHERE inv.codigo = C.codigo) - (
                                        ((SUM(inv.Cantidades)*(inv.CU)) +( 
                                        SUM(0) +(
                                        SELECT SUM((C.Cantidades)*(C.CU)) FROM compras1 AS C 
                                        WHERE inv.codigo = C.codigo))) / (
                                        (SUM(inv.Cantidades)) +(
                                        (SUM(0) +(
                                        SELECT SUM(C.Cantidades) FROM compras1 AS C
                                        WHERE inv.codigo = C.codigo))))  *(
                                        SUM(0) + (
                                        SELECT SUM(S.Cantidades) FROM salidas1 AS S
                                        WHERE inv.codigo = S.codigo)))
                                        AS Total3 
                                FROM inv_inicial AS inv
                                GROUP BY inv.codigo,inv.CU                             
                        ) A ON C.codigo = A.codigo       
                '''
        cur.execute(sql)
        table_rows = cur.fetchall()
        cur.close()     
        return table_rows
    


    def reportes_all_inventario1(self,codigo1,codigo2,codigo3,codigo4,codigo5,codigo6,codigo7,codigo8,codigo9,codigo10,
                                      codigo11,codigo12,codigo13,codigo14,codigo15,codigo16,codigo17,codigo18): 
        cur = self.conexion.cursor()
        sql = '''SELECT     
        I.codigo,
        I.Producto,
        I.Cantidades_iniciales,         
        I.CU_iniciales,
        I.Total_iniciales,                                      
        Cantidades1,                                
        CU_Compras,                 
        Total,                          
        Cantidades2,                            
        CU_Salidas,                         
        Total_Salidas,
        Inventario_Final,
        CU,
        Costo_total_Final
        FROM (SELECT inv.codigo,                    
                     inv.Producto,      
                     SUM(inv.Cantidades) AS Cantidades_iniciales,       
                     AVG(inv.CU) AS CU_iniciales,                           
                     SUM(inv.Cantidades) * AVG(inv.CU) AS Total_iniciales                           
                     FROM inv_inicial AS inv                    
                     WHERE inv.codigo IN (%s)                          
                     GROUP BY inv.codigo,inv.Producto       
                    ) I                
                    RIGHT JOIN (SELECT C.codigo, 
                                       SUM(C.Cantidades) AS Cantidades1,      
                                       AVG(C.CU) AS CU_Compras,                           
                                       SUM(C.Cantidades) * AVG(C.CU) AS Total                         
                                       FROM compras1 AS C                 
                                       WHERE C.codigo IN (%s)                                        
                  ) C ON C.codigo = I.codigo
                    RIGHT JOIN (SELECT S.codigo,                    
                                       SUM(S.Cantidades) AS Cantidades2    
                                       FROM salidas1 AS S                              
                                       WHERE S.codigo IN (%s) 
                                       GROUP BY S.codigo,S.CU  
                        ) S ON C.codigo = S.codigo              
                    RIGHT JOIN (SELECT AVG(C.CU) AS CU_Salidas                  
                                       FROM compras1 AS C 
                                       WHERE C.codigo IN (%s)                         
                                       GROUP BY Producto                           
                        ) K ON C.codigo = S.codigo              
                    RIGHT JOIN (SELECT (SUM(Cantidades)* '0' + (                    
                                        SELECT SUM(S.Cantidades) FROM salidas1 AS S  WHERE S.codigo IN (%s)))*AVG(C.CU) as Total_Salidas
                                        FROM compras1 AS C  
                                        WHERE C.codigo IN (%s)                         
                                        GROUP BY C.codigo                   
                        ) X ON C.codigo = S.codigo
                    RIGHT JOIN (SELECT  inv.codigo,
                                        (SUM(inv.Cantidades) +( 
                                        SELECT SUM(vc.Cantidades) FROM compras1 AS vc 
                                        WHERE vc .codigo IN (%s))-(
                                        SELECT SUM(S.Cantidades) FROM salidas1 AS S                                 
                                        WHERE S.codigo IN (%s))) AS Inventario_Final,
                                        (((SUM(0) +(                                
                                        SELECT (SUM((I.Cantidades)*(I .CU))) FROM inv_inicial AS I 
                                        WHERE I.codigo IN (%s))) +(
                                        ((SUM(0) +(                                
                                        SELECT (SUM((C.Cantidades)*(C.CU))) FROM compras1 AS C 
                                        WHERE C.codigo IN (%s)))) -(
                                        ((SUM(0) +(                                
                                        SELECT (SUM((S.Cantidades)*(S.CU))) FROM salidas1 AS S
                                        WHERE S.codigo IN (%s))))
                                        )))  /(
                                        (SUM(0) +( 
                                        SELECT SUM(I.Cantidades) FROM inv_inicial AS I 
                                        WHERE I.codigo IN (%s))+(
                                        (SUM(0) +( 
                                        SELECT SUM(C.Cantidades) FROM compras1 AS C 
                                        WHERE C.codigo IN (%s))-(
                                        (SUM(0) +( 
                                        SELECT SUM(S.Cantidades) FROM salidas1 AS S 
                                        WHERE S.codigo IN (%s))
                                        )))))))AS CU,
                                        ((SUM(0) +(                                
                                        SELECT (SUM((I.Cantidades)*(I .CU))) FROM inv_inicial AS I 
                                        WHERE I.codigo IN (%s))) +(
                                        (SUM(0) +( 
                                        SELECT (SUM((C.Cantidades)*(C.CU))) FROM compras1 AS C
                                        WHERE C.codigo IN (%s)))-(
                                        (SUM(0) +( 
                                        SELECT (SUM((S.Cantidades)*(S.CU))) FROM salidas1 AS S
                                        WHERE S.codigo IN (%s)))))) AS Costo_total_Final
                                        FROM inv_inicial AS inv
                                        WHERE inv.codigo IN (%s)
                                        GROUP BY inv.codigo
                        ) E ON C.codigo = E.codigo                          
                '''
        codigo1 = codigo1[0]
        codigo2 = codigo2[0]
        codigo3 = codigo3[0]
        codigo4 = codigo4[0]
        codigo5 = codigo5[0]
        codigo6 = codigo6[0]
        codigo7 = codigo7[0]
        codigo8 = codigo8[0]
        codigo9 = codigo9[0]
        codigo10 = codigo10[0]
        codigo11 = codigo11[0]
        codigo12 = codigo12[0]
        codigo13 = codigo13[0]
        codigo14 = codigo14[0]
        codigo15 = codigo15[0]
        codigo16 = codigo16[0]
        codigo17 = codigo17[0]
        codigo18 = codigo18[0]
        cur.execute(sql,(codigo1,codigo2,codigo3,codigo4,codigo5,codigo6,codigo7,codigo8,codigo9,codigo10,
                         codigo11,codigo12,codigo13,codigo14,codigo15,codigo16,codigo17,codigo18))
        nombreX = cur.fetchall()
        cur.close()     
        return nombreX



    def generar_inventario(self,desdelv,hastalv):
        cur = self.conexion.cursor()
        sql = """ SELECT * FROM compras1 WHERE Fecha BETWEEN %s AND %s"""
        desdelv = desdelv[0]
        hastalv = hastalv[0]
        cur.execute(sql,(desdelv,hastalv))
        datos = cur.fetchall() 
        return datos

    def generar_inventario_salidas(self,desdelv,hastalv):
        cur = self.conexion.cursor()
        sql = """ SELECT * FROM salidas1 WHERE Fecha BETWEEN %s AND %s"""
        desdelv = desdelv[0]
        hastalv = hastalv[0]
        cur.execute(sql,(desdelv,hastalv))
        datos = cur.fetchall() 
        return datos


    