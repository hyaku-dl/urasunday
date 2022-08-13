import setuptools

setuptools.setup(
    name="whine_md_fmt",
    entry_points={"mdformat.parser_extension": ["whine_md_fmt = main"]},
)
