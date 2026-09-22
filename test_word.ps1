try {
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    Write-Output "Word COM is successfully available! Version: $($word.Version)"
    $word.Quit()
} catch {
    Write-Output "Word COM error: $_"
}
