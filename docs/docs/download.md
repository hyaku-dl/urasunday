Module ura.download
===================

Functions
---------

    
`cr(rs: str) ‑> Callable[[int], bool]`
:   Returns a function that checks if the given int is within the range or not.
    The range is calculated from the given string.
    
    Args:
        rs (str): The range string where the range is calculated from.
    
    Returns:
        Callable[[int], bool]: The function that checks if the given int is within the range or not.

    
`get_extension(filename: str) ‑> str`
:   Get the file extension of a file from the given filename.
    
    Args:
        filename (str): The filename to get the file extension from.
    
    Returns:
        str: The file extension from the given filename.

    
`ordinal(n: int) ‑> str`
:   Convert the given number to ordinal number.
    
    Args:
        n (int): The number to convert into ordinal number.
    
    Returns:
        str: The said ordinal number.

    
`sanitize_filename(filename: str) ‑> str`
:   Sanitize the given filename.
    
    Args:
        filename (str): The filename to be sanitized.
    
    Returns:
        str: Sanitized filename.

Classes
-------

`DownloadFailed(*args, **kwargs)`
:   Common base class for all non-exit exceptions.

    ### Ancestors (in MRO)

    * builtins.Exception
    * builtins.BaseException

`Downloader(directory: str = None, overwrite: bool = True, **kwargs: Dict[str, Any])`
:   

    ### Methods

    `dlch(self, url: str)`
    :

    `dlf(self, file: List[str]) ‑> None`
    :   Individual image downloader.
        Args:
            file (str): List containing the filename and the url of the file.