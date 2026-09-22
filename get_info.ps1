Add-Type -AssemblyName System.Drawing
$files = Get-ChildItem -Path . -Filter *.jpeg
foreach ($file in $files) {
    $img = [System.Drawing.Image]::FromFile($file.FullName)
    Write-Output "$($file.Name) | $($img.Width)x$($img.Height) | $($img.PixelFormat) | $([math]::Round($file.Length/1024, 1)) KB"
    $img.Dispose()
}
