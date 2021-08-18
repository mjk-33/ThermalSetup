def decimal_str(x: float, decimals: int = 10) -> str:
    
    return format(x, f".{decimals}f").lstrip().rstrip('0')
