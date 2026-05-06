data = open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\index.html', 'rb').read()
lines = []
lines.append(f'File size: {len(data)}')
lines.append(f'Shanghai count: {data.count(b"上海麵".encode("utf-8"))}')
lines.append(f'Total cards: {data.count(b"<div class=\"p-card ")}')
lines.append(f'No-image: {data.count(b"p-card no-image")}')
lines.append('Done')
with open(r'C:\Users\admin\.qclaw\workspace\yauhing-food\result.txt', 'wb') as f:
    f.write('\n'.join(lines).encode('utf-8'))