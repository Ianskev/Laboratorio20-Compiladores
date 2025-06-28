# Compilador Laboratorio 20

Este proyecto es parte del curso de Compiladores en UTEC, laboratorio 20.

## Descripción

El proyecto implementa un compilador simple que incluye scanner, parser y visitor para procesar archivos de entrada y aplicar optimizaciones.

## Requisitos

- Python 3.x
- Compilador G++

## Estructura de archivos

- `main.cpp` - Punto de entrada del compilador
- `parser.cpp` - Implementación del parser
- `scanner.cpp` - Implementación del scanner
- `token.cpp` - Definición de tokens
- `visitor.cpp` - Implementación del patrón visitor
- `exp.cpp` - Definición de expresiones
- `make.py` - Script para compilar y ejecutar el programa
- `optimization.py` - Módulo de optimización

## Uso

Para compilar y ejecutar el proyecto con los archivos de entrada disponibles:

```bash
python make.py
```

El script realizará las siguientes acciones:
1. Compilar los archivos fuente
2. Procesar los archivos de entrada (input1.txt, input2.txt, input3.txt)
3. Aplicar optimizaciones a cada archivo de entrada
4. Ejecutar el programa con cada archivo optimizado

## Estructura de entrada

Los archivos de entrada deben ubicarse en la carpeta `inputs/` con los nombres input1.txt, input2.txt, e input3.txt.

## Autores

- [Tu nombre aquí]
