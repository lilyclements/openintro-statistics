$filePath = "source\ch05.ptx"
$content = Get-Content $filePath -Raw
$content = $content -replace ' xml:id=""', ''
Set-Content $filePath $content -NoNewline
Write-Host "Fixed $filePath - removed empty xml:id attributes"
