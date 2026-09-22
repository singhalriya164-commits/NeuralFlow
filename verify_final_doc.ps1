$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {
    $docPath = (Resolve-Path "NEURALFLOW_COMPLETE_PROJECT_REPORT.docx").Path
    $doc = $word.Documents.Open($docPath)
    Write-Host "=== NEURALFLOW_COMPLETE_PROJECT_REPORT.docx ==="
    Write-Host "Sections count: $($doc.Sections.Count)"
    for ($i = 1; $i -le $doc.Sections.Count; $i++) {
        $s = $doc.Sections.Item($i)
        Write-Host "Section $($i): Columns=$($s.PageSetup.TextColumns.Count), LeftMargin=$($s.PageSetup.LeftMargin), RightMargin=$($s.PageSetup.RightMargin), TopMargin=$($s.PageSetup.TopMargin), BottomMargin=$($s.PageSetup.BottomMargin)"
    }
    $pages = $doc.ComputeStatistics([Microsoft.Office.Interop.Word.WdStatistic]::wdStatisticPages)
    $words = $doc.ComputeStatistics([Microsoft.Office.Interop.Word.WdStatistic]::wdStatisticWords)
    $chars = $doc.ComputeStatistics([Microsoft.Office.Interop.Word.WdStatistic]::wdStatisticCharacters)
    $paragraphs = $doc.ComputeStatistics([Microsoft.Office.Interop.Word.WdStatistic]::wdStatisticParagraphs)
    Write-Host "Total Rendered Pages: $pages"
    Write-Host "Total Words: $words"
    Write-Host "Total Characters: $chars"
    Write-Host "Total Paragraphs: $paragraphs"
    $doc.Close([ref]$false)

    Write-Host "`n=== Checking c:\Users\Chaha\Downloads\Project-template-a4.docx ==="
    $dlDocPath = "c:\Users\Chaha\Downloads\Project-template-a4.docx"
    $dlDoc = $word.Documents.Open($dlDocPath)
    $dlPages = $dlDoc.ComputeStatistics([Microsoft.Office.Interop.Word.WdStatistic]::wdStatisticPages)
    Write-Host "Downloads Doc Rendered Pages: $dlPages"
    Write-Host "Downloads Doc Section 4 Columns: $($dlDoc.Sections.Item(4).PageSetup.TextColumns.Count)"
    $dlDoc.Close([ref]$false)
} finally {
    $word.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
}
