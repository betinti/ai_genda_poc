def file_to_string(file_path: str):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        print(f"Erro ao ler o arquivo {file_path}: {e}")
        return None

def try_to_read_files(file_path: str) -> bool:
    """
    Tenta abrir um arquivo para leitura e retorna True se for possível, False caso contrário.
    """
    print(f"Tentando ler o arquivo: {file_path}")
    try:
        with open(file_path, 'r') as f:
            pass
        return True
    except Exception as e:
        print(f"Não foi possível ler o arquivo '{file_path}': {e}")
        return False