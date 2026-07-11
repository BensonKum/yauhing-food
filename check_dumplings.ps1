$lines = Get-Content index.html -Encoding UTF8
for($i=378;$i -le 420;$i++){
    $line = $lines[$i]
    $stripped = $line -replace '<[^>]+>',''
    if($stripped.Trim().Length -gt 0){
        Write-Output "$($i+1): $stripped"
    }
}
