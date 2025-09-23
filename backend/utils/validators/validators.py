def isPDF(file: bytes) -> bool:
    return file.startswith(b"%PDF-") # TODO: implementar isto na rota de /save-pdf