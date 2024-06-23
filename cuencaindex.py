
#Función que añade a archivo vectorial información morfométrica y topográfica
#se requiere DEM


def cuencaindex(dem,cuencaInput,morfoCuenca):

    import processing   
    
    #Entradas
    dem=r"C:\Users\exequ\Documents\Contenedor_Scripts\DEM.tif"
    cuencaInput=r"C:\Users\exequ\Documents\Contenedor_Scripts\cuencas.gpkg"
    morfoOutput=r'C:\Users\exequ\Documents\Contenedor_Scripts\morfoOutput.gpkg'


    #Cálculo de Área en km2

    areaVector=processing.run("native:fieldcalculator",
    {'INPUT':cuencaInput,
    'FIELD_NAME':'AREA_KM2',
    'FIELD_TYPE':0,
    'FIELD_LENGTH':0,
    'FIELD_PRECISION':0,
    'FORMULA':'$area /1000000',
    'OUTPUT':'TEMPORARY_OUTPUT',
    '--overwrite':True})

    print("Area Terminada")
        
    #Cálculo del Perímetro en km

    perimetroVector=processing.run("native:fieldcalculator",
    {'INPUT':areaVector['OUTPUT'],
    'FIELD_NAME':'PER_KM',
    'FIELD_TYPE':0,
    'FIELD_LENGTH':0,
    'FIELD_PRECISION':0,
    'FORMULA':' $perimeter /1000',
    'OUTPUT':'TEMPORARY_OUTPUT',
    '--overwrite':True})

    print("Perimetro Terminado")

    #Calculo de pendientes

    pendiente=processing.run("native:slope", 
    {'INPUT':dem,
    'Z_FACTOR':1,
    'OUTPUT':'TEMPORARY_OUTPUT',
    '--overwrite':True})


    print("Pendiente Terminada")


     Estadistica zonal altitud

    estAltitud=processing.run("native:zonalstatisticsfb", 
    {'INPUT':perimetroVector['OUTPUT'],
    'INPUT_RASTER':dem,
    'RASTER_BAND':1,
    'COLUMN_PREFIX':'ALT_',
    'STATISTICS':[2,5,6],
    'OUTPUT':'TEMPORARY_OUTPUT',
    '--overwrite':True})

    print("Estadistica Zonal Altitud Terminada")


    #Estadstica zona pendiente

    estPend=processing.run("native:zonalstatisticsfb", 
    {'INPUT':estAltitud['OUTPUT'],
    'INPUT_RASTER':pendiente['OUTPUT'],
    'RASTER_BAND':1,
    'COLUMN_PREFIX':'PEND_',
    'STATISTICS':[2,5,6],
    'OUTPUT':'TEMPORARY_OUTPUT',
    '--overwrite':True})

    print("Estadistica Zonal Pend.Terminada")


    #Relieve de la Cuenca en Km

    relieveVector=processing.run("native:fieldcalculator", 
    {'INPUT':estPend['OUTPUT'],
    'FIELD_NAME':'REL_Km',
    'FIELD_TYPE':0,
    'FIELD_LENGTH':0,
    'FIELD_PRECISION':2,
    'FORMULA':' "ALT_max" - "ALT_min" ',
    'OUTPUT':'TEMPORARY_OUTPUT',
    '--overwrite':True})

    print("Relieve Terminado")

    #Circularidad de la Cuenca

    circCuenca=processing.run("native:fieldcalculator",
    {'INPUT':relieveVector['OUTPUT'],
    'FIELD_NAME':'Circ_Cuenca',
    'FIELD_TYPE':0,
    'FIELD_LENGTH':0,
    'FIELD_PRECISION':2,
    'FORMULA':'(4*pi()*"AREA_KM2")/("PER_KM")^2',
    'OUTPUT':'TEMPORARY_OUTPUT',
    '--overwrite':True})

    print("Circulardad Terminada")

    #Cálculo del número de rugosidad de Meltons

    MRN=processing.run("native:fieldcalculator", 
    {'INPUT':circCuenca['OUTPUT'],
    'FIELD_NAME':'MRN',
    'FIELD_TYPE':0,
    'FIELD_LENGTH':0,
    'FIELD_PRECISION':2,
    'FORMULA':'("REL_Km")*("AREA_KM2"^-0.5)',
    'OUTPUT':'TEMPORARY_OUTPUT',
    '--overwrite':True})

    print("Rugosidad Terminada")


    #Clasificación Rugosidad

    processing.run("native:fieldcalculator",
    {'INPUT':MRN['OUTPUT'],
     'FIELD_NAME': 'CLASS_MRN',
        'FIELD_TYPE': 2,
        'FIELD_LENGTH': 20, 
        'FIELD_PRECISION': 0,
        'FORMULA': "CASE WHEN \"MRN\" <= 1 THEN 'Superficie suave' "
                   "WHEN \"MRN\" > 1 AND \"MRN\" <= 10 THEN 'Superficie moderada' "
                   "WHEN \"MRN\" > 10 THEN 'Superficie rugosa' "
                   "ELSE 'No definido' END",
        'OUTPUT':morfoOutput,
        '--overwrite': True
    })

    print("Clasificación de rugosidad terminada")
        
















