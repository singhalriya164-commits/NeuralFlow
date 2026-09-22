$word = [System.Runtime.InteropServices.Marshal]::GetActiveObject('Word.Application')
Write-Host "Word Documents Open: $($word.Documents.Count)"
foreach ($doc in $word.Documents) {
    Write-Host "Doc Name: $($doc.Name), FullName: $($doc.FullName)"
    Write-Host "Pages: $($doc.ComputeStatistics([Microsoft.Office.Interop.Word.WdStatistic]::wdStatisticPages))"
    Write-Host "Sections: $($doc.Sections.Count)"
    for ($i=1; $i -le $doc.Sections.Count; $i++) {
        $sec = $doc.Sections.Item($i)
        Write-Host "  Section $($i) : Columns=$($sec.PageSetup.TextColumns.Count), LeftMargin=$($sec.PageSetup.LeftMargin), RightMargin=$($sec.PageSetup.RightMargin)"
    }
}
