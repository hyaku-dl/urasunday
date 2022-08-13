if ( Test-Path -Path pyenv\ )
{
    . .\pyenv\Scripts\Activate.ps1
}

function dev
{
    param(
        $Command
    )

    if (!$Command) {
        foreach($_ in Get-ChildItem $PSScriptRoot\dev\scripts\ps1\ -Name) {
            [System.IO.Path]::GetFileNameWithoutExtension($_)
        }
        return
    }

    & "$PSScriptRoot\dev\scripts\ps1\$Command.ps1" @args
}
