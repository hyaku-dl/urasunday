# **[ura](../index.md).[src](../src.md).[download](download.md)**

## **Functions**

<h3><b><a href="#func-get_extension" id="func-get_extension">get_extension</a></b></h3>

```python
(filename: str) ‑> str
```

Get the file extension of a file from the given filename.

<h3><b><i><a href="#func-get_extension-args" id="func-get_extension-args">Args:</a></i></b></h3>

- filename (`str`): The filename to get the file extension from.

<h3><b><i><a href="#func-get_extension-returns" id="func-get_extension-returns">Returns:</a></i></b></h3>

`str`: The file extension from the given filename.

<h3><b><a href="#func-get_stg" id="func-get_stg">get_stg</a></b></h3>

```python
(path: str, de: Any = None)
```

<h3><b><a href="#func-sanitize_filename" id="func-sanitize_filename">sanitize_filename</a></b></h3>

```python
(filename: str) ‑> str
```

Sanitize the given filename.

<h3><b><i><a href="#func-sanitize_filename-args" id="func-sanitize_filename-args">Args:</a></i></b></h3>

- filename (`str`): The filename to be sanitized.

<h3><b><i><a href="#func-sanitize_filename-returns" id="func-sanitize_filename-returns">Returns:</a></i></b></h3>

`str`: Sanitized filename.

## **Classes**

<h3><b><a href="#class-Downloader" id="class-Downloader">Downloader</a></b></h3>

```python
(directory: str = None, overwrite: bool = None, **kwargs: Dict[str, Any])
```

<h3><b><i><a href="#class-Downloader-func" id="class-Downloader-func">Methods</a></i></b></h3>

<h3><i><a href="#class-Downloader-func-dlch" id="class-Downloader-func-dlch">dlch</a></i></h3>

```python
(self, url: str)
```

<h3><i><a href="#class-Downloader-func-dlf" id="class-Downloader-func-dlf">dlf</a></i></h3>

```python
(self, file: List[str])
```

Individual image downloader.

<h3><a href="#class-Downloader-func-dlf-args" id="class-Downloader-func-dlf-args">Args:</a></h3>

- file (`str`): List containing the filename and the url of the file.
