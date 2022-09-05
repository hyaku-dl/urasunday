<h1 align="center" style="font-weight: bold">
    Changelog
</h1>

<h2 id="0-0-0-0-2-0">0.0.0.0-rc.0</h2>

## Added

- `-on`/`--overwrite_not`, `-op`/`--overwrite_prompt`, and `-opn`/`--overwrite_prompt_not` flags for the `dl` subcommand.

<h3 id="0-0-0-0-2-0-added">Added</h3>

- `-on`/`--overwrite_not`, `-op`/`--overwrite_prompt`, and `-opn`/`--overwrite_prompt_not` flags for the `dl` subcommand.

<h3 id="0-0-0-0-2-0-changed">Changed</h3>

- Made the app log the `log path` even when loading, so that the user will know where to find the said file when it gets stuck while loading.

- .AppImage so that you can run the cli by appending the `cli` subcommand to the command for running the said AppImage. For example, `./ura.AppImage cli [flags]`.

<h3 id="0-0-0-0-2-0-fixed">Fixed</h3>

- `overwrite` settings not being followed (i.e. `overwrite` set to False, yet the chapter that is already downloaded is being overwritten).

- Once and for all, the fucking python imports, for fuck's sake.

- Improved documentation!

<h2 id="0-0-0-0-1-1">0.0.0.0-beta.1</h2>

## Added

- Dynamic version and copyright information

<h3 id="0-0-0-0-1-1-added">Added</h3>

- Dynamic version and copyright information

<h3 id="0-0-0-0-1-1-changed">Changed</h3>

- Improved logging

<h3 id="0-0-0-0-1-1-fixed">Fixed</h3>

- Incorrect python library importing that causes the app to crash outright

<h2 id="0-0-0-0-1-0">0.0.0.0-beta.0</h2>

<b><font color="#ED5E5E">YANKED!</font></b>

<h3 id="0-0-0-0-1-0-added">Added</h3>

- Icon for .AppImage distribution of that app

- Logging information to help debug the application

- The app now reflects changes made on the configuration file on the app

<h3 id="0-0-0-0-1-0-changed">Changed</h3>

- Improved loading of the app, so that when the loading page is removed, the app is totally usable

- Uses parts of private project (`whinee/snippets.py`) for the configuration of the app, and others

<h2 id="0-0-0-0-0-5">0.0.0.0-alpha.5</h2>

## Added

- Loading screen for app initialization

<h3 id="0-0-0-0-0-5-added">Added</h3>

- Loading screen for app initialization

<h3 id="0-0-0-0-0-5-fixed">Fixed</h3>

- AppImages to be marked as AppImages (means that the config now goes on the config folder instead of the same directory as the AppImage)

<h2 id="0-0-0-0-0-4">0.0.0.0-alpha.4</h2>

<b><font color="#ED5E5E">YANKED!</font></b>

<h3 id="0-0-0-0-0-4-added">Added</h3>

- Initialization of configuration file

<h2 id="0-0-0-0-0-3">0.0.0.0-alpha.3</h2>

<b><font color="#ED5E5E">YANKED!</font></b>

<h3 id="0-0-0-0-0-3-fixed">Fixed</h3>

- `vls` string on `ura/__init__.py` to `[0, 0, 0, 0, 0, 3]`

<h2 id="0-0-0-0-0-2">0.0.0.0-alpha.2</h2>

<b><font color="#ED5E5E">YANKED!</font></b>

<h3 id="0-0-0-0-0-2-fixed">Fixed</h3>

- Unquoted `__version__` string on `ura/__init__.py`

<h2 id="0-0-0-0-0-1">0.0.0.0-alpha.1</h2>

<h3 id="0-0-0-0-0-1-removed">Removed</h3>

- Useless imports

<h2 id="0-0-0-0-0-0">0.0.0.0-alpha.0</h2>
