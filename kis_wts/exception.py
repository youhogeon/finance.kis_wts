class KisWtsException(Exception):
    """Base exception for KisWts errors."""
    
    def __init__(self, message: str):
        super().__init__(message)
        
        self.message = message