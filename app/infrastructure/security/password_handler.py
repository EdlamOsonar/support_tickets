"""Manejo de contraseñas."""
from passlib.context import CryptContext

# Contexto de encriptación para contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica si la contraseña en texto plano coincide con el hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Genera hash bcrypt de la contraseña.
    
    Bcrypt tiene un límite de 72 bytes. Si la contraseña es más larga,
    se valida y se lanza un error claro.
    """
    # Asegurarse de que la contraseña es una cadena
    if not isinstance(password, str):
        raise ValueError("La contraseña debe ser una cadena de texto")
    
    # Convertir a bytes para verificar la longitud real
    password_bytes = password.encode('utf-8')
    password_length_bytes = len(password_bytes)
    
    # Validar longitud antes de pasar a passlib
    if password_length_bytes > 72:
        raise ValueError(
            f"La contraseña no puede tener más de 72 bytes. "
            f"Tu contraseña tiene {password_length_bytes} bytes. "
            f"Por favor, usa una contraseña más corta."
        )
    
    # Intentar hacer el hash, capturando errores de passlib
    try:
        return pwd_context.hash(password)
    except ValueError as e:
        # Capturar errores específicos de passlib sobre longitud
        error_msg = str(e)
        if "72 bytes" in error_msg.lower() or "truncate" in error_msg.lower():
            raise ValueError(
                f"La contraseña excede el límite de 72 bytes de bcrypt. "
                f"Tu contraseña tiene {password_length_bytes} bytes. "
                f"Por favor, usa una contraseña más corta. "
                f"Ejemplo de formato válido: (Aion__2025)"
            ) from e
        # Re-lanzar otros errores de ValueError
        raise

