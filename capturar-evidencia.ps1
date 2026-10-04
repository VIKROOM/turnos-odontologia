# Captura de pantalla completa y la guarda con el nombre que le pidas.
# Uso (PowerShell, desde la raiz del repo):
#   .\capturar-evidencia.ps1 "docs\etapa0\01-instalador-full.png"

param(
    [Parameter(Mandatory = $true)][string]$Ruta,
    [int]$RetardoSegundos = 0
)

Add-Type -AssemblyName System.Windows.Forms, System.Drawing

if ($RetardoSegundos -gt 0) { Start-Sleep -Seconds $RetardoSegundos }

$dir = Split-Path -Parent $Ruta
if ($dir -and -not (Test-Path -LiteralPath $dir)) {
    New-Item -ItemType Directory -Path $dir -Force | Out-Null
}

$b = [System.Windows.Forms.SystemInformation]::VirtualScreen
$bmp = New-Object System.Drawing.Bitmap $b.Width, $b.Height
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.CopyFromScreen($b.Left, $b.Top, 0, 0, $bmp.Size)
$g.Dispose()

$bmp.Save((Join-Path (Get-Location) $Ruta), [System.Drawing.Imaging.ImageFormat]::Png)
$bmp.Dispose()

$kb = [math]::Round((Get-Item -LiteralPath $Ruta).Length / 1KB, 1)
Write-Output "OK  $Ruta  ($([math]::Round($b.Width))x$([math]::Round($b.Height)) px, $kb KB)"