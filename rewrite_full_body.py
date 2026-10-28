import re

# 1. Read FaceCaptureScreen
with open('app/src/main/java/com/example/emiyo/feature/capture/FaceCaptureScreen.kt', 'r') as f:
    code = f.read()

# Replace texts
code = code.replace("fun FaceCaptureScreen(", "fun FullBodyCaptureScreen(")
code = code.replace('text = "FACE CAPTURE"', 'text = "FULL BODY CAPTURE"')
code = code.replace('text = "Let’s capture\\nyour face."', 'text = "Let’s capture\\nyour silhouette."')
code = code.replace('text = "Take a clear photo of your face in natural light."', 'text = "Take a few full-body photos from different angles so we can understand your proportions, silhouette and fit."')
code = code.replace("FaceCaptureStandardPreview()", "FullBodyCaptureStandardPreview()")
code = code.replace("FaceCaptureScreen()", "FullBodyCaptureScreen()")

# Save to FullBodyCaptureScreen
with open('app/src/main/java/com/example/emiyo/feature/capture/FullBodyCaptureScreen.kt', 'w') as f:
    f.write(code)

# 2. HTML Replace
with open('preview/face_capture_preview.html', 'r') as f:
    html = f.read()

html = html.replace("<title>WARDROBE - Face Capture (Screen 12)</title>", "<title>WARDROBE - Full Body Capture (Screen 13)</title>")
html = html.replace('<span class="section-label">FACE CAPTURE</span>', '<span class="section-label">FULL BODY CAPTURE</span>')
html = html.replace('<h1 class="editorial-headline">Let’s capture<br>your face.</h1>', '<h1 class="editorial-headline">Let’s capture<br>your silhouette.</h1>')
html = html.replace('<p class="description-text">Take a clear photo of your face in natural light.</p>', '<p class="description-text">Take a few full-body photos from different angles so we can understand your proportions, silhouette and fit.</p>')

with open('preview/full_body_capture_preview.html', 'w') as f:
    f.write(html)
