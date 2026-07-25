Add-Type -AssemblyName System.Drawing
$src = "C:\Users\admin\.qclaw\media\inbound\c729a16d-f79f-479e-8e7c-43179da66731.jpg"
$out = "C:\Users\admin\.qclaw\workspace\yauhing-food\images\product_cabbage_dumpling.jpg"
$img = [System.Drawing.Image]::FromFile($src)
$w = $img.Width
$h = $img.Height
$side = [Math]::Min($w, $h)
$x = [int][Math]::Floor(($w - $side) / 2)
$y = [int][Math]::Floor(($h - $side) / 2)
$crop = New-Object System.Drawing.Rectangle($x, $y, $side, $side)
$bmp = New-Object System.Drawing.Bitmap(800, 800)
$g = [System.Drawing.Graphics]::FromImage($bmp)
$g.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
$g.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
$g.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality
$g.DrawImage($img, (New-Object System.Drawing.Rectangle(0, 0, 800, 800)), $crop, [System.Drawing.GraphicsUnit]::Pixel)
$enc = [System.Drawing.Imaging.ImageCodecInfo]::GetImageEncoders() | Where-Object { $_.MimeType -eq "image/jpeg" }
$qual = New-Object System.Drawing.Imaging.EncoderParameters(1)
$qual.Param[0] = New-Object System.Drawing.Imaging.EncoderParameter([System.Drawing.Imaging.Encoder]::Quality, [long]85)
$bmp.Save($out, $enc, $qual)
Write-Host ("Source " + $w + "x" + $h + " | crop " + $side + "x" + $side + "@(" + $x + "," + $y + ") | saved 800x800")
$img.Dispose()
$g.Dispose()
$bmp.Dispose()
