def cuencastat(dem,cuencas,sizekm2):
    
    #Librerias
    
    import proccesing
    import rasterio as rs
    
    #Entradas

    dem=r"C:\Users\exequ\Documents\Contenedor_Scripts\DEM.tif"
    cuencas=r"C:\Users\exequ\Documents\Contenedor_Scripts\cuencas.shp"
    sizekm2=10

    # Tamano de cuenca

    demMeta=rs.open(dem)
    resolucionArea= demMeta.res[0]*demMeta.res[1]
    area=(sizekm2*1000000)/resolucionArea


    #Delimitacion de cuenca

    delimitCuenca=processing.run("grass7:r.watershed",
        {'elevation':dem,
        'depression':None,
        'flow':None,
        'disturbed_land':None,
        'blocking':None,
        'threshold':area,
        'max_slope_length':None,
        'convergence':5,
        'memory':300,
        '-s':False,
        '-m':False,
        '-4':False,
        '-a':False,
        '-b':False,
        'accumulation':'TEMPORARY_OUTPUT',
        'drainage':'TEMPORARY_OUTPUT',
        'basin':'TEMPORARY_OUTPUT',
        'stream':'TEMPORARY_OUTPUT',
        'half_basin':'TEMPORARY_OUTPUT',
        'length_slope':'TEMPORARY_OUTPUT',
        'slope_steepness':'TEMPORARY_OUTPUT',
        'tci':'TEMPORARY_OUTPUT',
        'spi':'TEMPORARY_OUTPUT',
        'GRASS_REGION_PARAMETER':None,
        'GRASS_REGION_CELLSIZE_PARAMETER':0,
        'GRASS_RASTER_FORMAT_OPT':'',
        'GRASS_RASTER_FORMAT_META':'',
        '--overwrite':True})


    print("delimitacion_terminada")


    #Poligonizar cuenca

    poliCuenca=processing.run("gdal:polygonize", 
        {'INPUT':delimitCuenca['basin'],
        'BAND':1,
        'FIELD':'DN',
        'EIGHT_CONNECTEDNESS':False,
        'EXTRA':'',
        'OUTPUT':'TEMPORARY_OUTPUT',
        '--overwrite':True})

    print("poligonizacion terminada")


    #Corregir geometria

    cuencaVectorCorr=processing.run("native:fixgeometries",
        {'INPUT':poliCuenca['OUTPUT'],
        'METHOD':1,
        'OUTPUT':'TEMPORARY_OUTPUT',
        '--overwrite':True})

    print("geometria_terminada")

    #Calculo de pendientes

    pendiente=processing.run("native:slope", 
        {'INPUT':dem,
        'Z_FACTOR':1,
        'OUTPUT':'TEMPORARY_OUTPUT',
        '--overwrite':True})

    print("Pendiente Terminada")


    #Estadistica zonal altitud

    estAltitud=processing.run("native:zonalstatisticsfb", 
        {'INPUT':cuencaVectorCorr['OUTPUT'],
        'INPUT_RASTER':dem,
        'RASTER_BAND':1,
        'COLUMN_PREFIX':'Alt_',
        'STATISTICS':[2,5,6],
        'OUTPUT':'TEMPORARY_OUTPUT',
        '--overwrite':True})

    print("Estadistica Zonal Altitud Terminada")


    #Estadstica zona pendiente

    processing.run("native:zonalstatisticsfb", 
        {'INPUT':estAltitud['OUTPUT'],
        'INPUT_RASTER':pendiente['OUTPUT'],
        'RASTER_BAND':1,
        'COLUMN_PREFIX':'Pen_',
        'STATISTICS':[2,0,0],
        'OUTPUT':cuencas,
        '--overwrite':True})

    print("Estadistica Zonal Pend.Terminada")

