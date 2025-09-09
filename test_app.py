def saludar(nombre: str) -> str:
    return f"Hola, {nombre}"

def test_saludar():
    assert saludar("Luis") == "Hola, Luis"
