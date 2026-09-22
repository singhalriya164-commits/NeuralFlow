$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {
    $docPath = (Resolve-Path "test_template_output.docx").Path
    $doc = $word.Documents.Open($docPath)
    Write-Host "Sections count: $($doc.Sections.Count)"
    for ($i = 1; $i -le $doc.Sections.Count; $i++) {
        $s = $doc.Sections.Item($i)
        Write-Host "Section $($i): Columns=$($s.PageSetup.TextColumns.Count), StartType=$($s.PageSetup.SectionStart)"
    }
    $pages = $doc.ComputeStatistics([Microsoft.Office.Interop.Word.WdStatistic]::wdStatisticPages)
    Write-Host "Pages count: $pages"
    $doc.Close([ref]$false)
} finally {
    $word.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
}
