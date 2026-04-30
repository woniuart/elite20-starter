from pypdf import PdfReader

pdf_path = r'c:/Users/16485/CodeBuddy/20260428093917/Week01-02_Outline_CN.pdf'

reader = PdfReader(pdf_path)
print(f"总页数: {len(reader.pages)}")

for i, page in enumerate(reader.pages):
    print(f'\n=== 第 {i+1} 页 ===')
    text = page.extract_text()
    if text:
        print(text)
    else:
        print('（无文本）')
