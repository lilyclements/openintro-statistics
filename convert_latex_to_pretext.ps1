# Script to convert remaining LaTeX commands in ch05.ptx to PreTeXt XML

$filePath = "source\ch05.ptx"
$content = Get-Content $filePath -Raw

# 1. Convert $...$ to <m>...</m> for inline math
# Pattern: $...$ where ... doesn't contain line breaks
$content = $content -replace '\$([^$\n]+)\$', '<m>$1</m>'

# 2. Fix any \footnotetext commands (convert to comments or keep as-is if already processed)
# These are already handled by manual edits, but ensure they're not doubled

# 3. Convert \termsub{term}{definition} to <term>term</term>
# This is a complex macro, for now just extract the term
$content = $content -replace '\\termsub\{([^}]+)\}\{[^}]+\}', '<term>$1</term>'

# 4. Convert \emph{text} to <em>text</em>
$content = $content -replace '\\emph\{([^}]+)\}', '<em>$1</em>'

# 5. Convert remaining \footnote (should be minimal) to <fn>
$content = $content -replace '\\footnote\{', '<fn>'

# Write back
Set-Content $filePath $content -NoNewline
Write-Host "Converted LaTeX commands in $filePath"
