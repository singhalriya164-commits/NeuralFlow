$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {
    $doc = $word.Documents.Open((Resolve-Path "NEURALFLOW_COMPLETE_PROJECT_REPORT.docx").Path)
    $pages = $doc.ComputeStatistics([Microsoft.Office.Interop.Word.WdStatistic]::wdStatisticPages)
    Write-Host "Total Pages: $pages"
    
    # Go to end of document
    $endRange = $doc.Range($doc.Content.End - 1, $doc.Content.End - 1)
    $pageOfEnd = $endRange.Information([Microsoft.Office.Interop.Word.WdInformation]::wdActiveEndPageNumber)
    $lineOfEnd = $endRange.Information([Microsoft.Office.Interop.Word.WdInformation]::wdFirstCharacterLineNumber)
    Write-Host "End of doc is on Page: $pageOfEnd, Line: $lineOfEnd"
    
    $doc.Close([ref]$false)
} finally {
    $word.Quit()
    [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
}
