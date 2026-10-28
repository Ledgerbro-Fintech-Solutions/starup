with open('app/src/main/java/com/example/emiyo/feature/capture/FullBodyCaptureScreen.kt', 'r') as f:
    code = f.read()

code = code.replace("R.drawable.face_capture_demo", "R.drawable.full_body_capture_demo")
with open('app/src/main/java/com/example/emiyo/feature/capture/FullBodyCaptureScreen.kt', 'w') as f:
    f.write(code)

with open('preview/full_body_capture_preview.html', 'r') as f:
    html = f.read()

html = html.replace("face_capture_demo.png", "full_body_background.png")
with open('preview/full_body_capture_preview.html', 'w') as f:
    f.write(html)
