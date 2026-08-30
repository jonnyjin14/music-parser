# bob-setup.ps1
# Copies the .bob configuration (custom modes, skills, and rules) into a target repository.
# Usage:
#   .\bob-setup.ps1 -Target "C:\path\to\other-repo"
#   .\bob-setup.ps1                    # defaults to current directory

param(
    [string]$Target = "."
)

$source = Join-Path $PSScriptRoot ".bob"
$dest   = Join-Path $Target ".bob"

if (-not (Test-Path $source)) {
    Write-Error "Source .bob directory not found at: $source"
    exit 1
}

if (-not (Test-Path $Target)) {
    Write-Error "Target directory does not exist: $Target"
    exit 1
}

Write-Host "Copying .bob configuration to: $dest" -ForegroundColor Cyan

Copy-Item -Path $source -Destination $dest -Recurse -Force

Write-Host ""
Write-Host "Done. The following were installed:" -ForegroundColor Green
Get-ChildItem -Path $dest -Recurse -File | ForEach-Object {
    Write-Host "  $($_.FullName.Replace($Target, '').TrimStart('\/'))"
}

Write-Host ""
Write-Host "Note: The rules files in .bob\rules-agent\, .bob\rules-ask\, and .bob\rules-plan\" -ForegroundColor Yellow
Write-Host "      contain project-specific notes for this repo. Edit them for your new project." -ForegroundColor Yellow
