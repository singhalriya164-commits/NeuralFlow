$word = New-Object -ComObject Word.Application
$word.Visible = $false
$doc = $word.Documents.Open('C:\Users\Chaha\OneDrive\Desktop\NeuralFlow\NEURALFLOW_COMPLETE_PROJECT_REPORT.docx')
Write-Output "Sections count: $($doc.Sections.Count)"
for ($i = 1; $i -le $doc.Sections.Count; $i++) {
    $s = $doc.Sections.Item($i)
    Write-Output "Section $i has $($s.PageSetup.TextColumns.Count) columns"
}
$doc.Close([ref]$false)
$word.Quit()
