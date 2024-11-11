from transformers import LayoutLMForTokenClassification, LayoutLMTokenizer

tokenizer = LayoutLMTokenizer.from_pretrained("D:/receipt_extract/SROIE2019/layoutlm-base-uncased")
model = LayoutLMForTokenClassification.from_pretrained("D:/receipt_extract/SROIE2019/layoutlm-base-uncased")
print("Model and tokenizer loaded successfully!")
