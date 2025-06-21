def extract_num(s: str) -> int:
    """
    Extracts the first integer from a string.
    
    Args:
        s (str): The input string from which to extract the integer.
        
    Returns:
        int: The first integer found in the string, or 0 if no integer is found.
    """
    num = ''.join(filter(str.isdigit, s))
    return int(num) if num else 0