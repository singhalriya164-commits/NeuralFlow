$docxPath = "C:\Users\Chaha\OneDrive\Desktop\NeuralFlow\NEURALFLOW_COMPLETE_PROJECT_REPORT.docx"

try {
    $word = New-Object -ComObject Word.Application
    $word.Visible = $false
    $doc = $word.Documents.Open($docxPath)
    
    # Force pagination update
    $doc.Repaginate()
    
    $pages = $doc.ComputeStatistics(2) # 2 = wdStatisticPages
    $words = $doc.ComputeStatistics(0) # 0 = wdStatisticWords
    $paras = $doc.Paragraphs.Count
    $tables = $doc.Tables.Count
    $inlineShapes = $doc.InlineShapes.Count
    
    Write-Output "=== MICROSOFT WORD VERIFICATION ==="
    Write-Output "Exact Rendered Pages: $pages"
    Write-Output "Total Word Count: $words"
    Write-Output "Total Paragraphs: $paras"
    Write-Output "Total Tables: $tables"
    Write-Output "Total Inline Shapes (Images): $inlineShapes"
    
    $doc.Close([ref]$false)
    $word.Quit()
} catch {
    Write-Output "Error: $_"
    if ($word) { $word.Quit() }
}
