import subprocess
import os
from optimization import optimize

# Carpeta de entrada
input_dir = "inputs"

# Archivos fuente
source_files = [
    "main.cpp", "parser.cpp", "scanner.cpp", "token.cpp",
    "visitor.cpp", "exp.cpp"
]

# Compilar
print("Compilando...")
compile_cmd = ["g++"] + source_files
result = subprocess.run(compile_cmd)

if result.returncode != 0:
    print("Error de compilación.")
    exit(1)

print("Compilación exitosa.\n")

for i in range(1, 4):
    
    input_file = os.path.join(input_dir, f"input{i}.txt")


    if not os.path.exists(input_file):
        print(f"{input_dir} no existe. Se omite.")
        continue
    input_file_processed = os.path.join(input_dir, f"input{i}_processed.txt")
    optimize(input_file, input_file_processed)

    print(f"\nEjecutando con {input_file_processed}")
    subprocess.run(["./a.exe", input_file_processed])