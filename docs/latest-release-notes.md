<h1 align="center" style="font-weight: bold">
    0.0.0.0-rc.0
</h1>

## **Description**

Pre-release identifier bump.

## **<a href="#0-0-0-0-2-0-added" id="0-0-0-0-2-0-added">Added</a>**

- `-on`/`--overwrite_not`, `-op`/`--overwrite_prompt`, and `-opn`/`--overwrite_prompt_not` flags for the `dl` subcommand.

## **<a href="#0-0-0-0-2-0-changed" id="0-0-0-0-2-0-changed">Changed</a>**

- Made the app log the `log path` even when loading, so that the user will know where to find the said file when it gets stuck while loading.

- .AppImage so that you can run the cli by appending the `cli` subcommand to the command for running the said AppImage. For example, `./ura.AppImage cli [flags]`.

## **<a href="#0-0-0-0-2-0-fixed" id="0-0-0-0-2-0-fixed">Fixed</a>**

- `overwrite` settings not being followed (i.e. `overwrite` set to False, yet the chapter that is already downloaded is being overwritten).

- Once and for all, the fucking python imports, for fuck's sake.

- Improved documentation!
