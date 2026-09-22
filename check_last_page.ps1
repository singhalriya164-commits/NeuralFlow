$docxPath = "C:\Users\Chaha\OneDrive\Desktop\NeuralFlow\NEURALFLOW_COMPLETE_PROJECT_REPORT.docx"
$word = New-Object -ComObject Word.Application
$word.Visible = $false
$doc = $word.Documents.Open($docxPath)
$pages = $doc.ComputeStatistics(2)
Write-Output "Total Pages: $pages"

# Check how full the last page is by checking selection or lines
$selection = $word.Selection
$doc.Characters.Last.Select()
$pageOfEnd = $word.Selection.Information(3) # 3 = wdActiveEndPageNumber
$lineOfEnd = $word.Selection.Information(10) # 10 = wdFirstCharacterLineNumber
Write-Output "End character is on page: $pageOfEnd, line: $lineOfEnd"

$doc.Close([ref]$false)
$word.Quit()
