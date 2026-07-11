$content = Get-Content inventory.html -Encoding UTF8 -Raw
$pattern = 'isFreshNoodle1Plus1'
$idx = 0
while(($idx = $content.IndexOf($pattern, $idx)) -ge 0){
    $line = 1 + ($content.Substring(0,$idx).Split("`n").Count - 1)
    Write-Output "Line $line: $($content.Substring([Math]::Max(0,$idx-30), 80).Replace("`n",''))"
    $idx += $pattern.Length
}
