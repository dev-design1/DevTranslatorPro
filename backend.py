from deep_translator import GoogleTranslator

def translate_text(text, source, target):
    """
    Translate text using Google Translator
    
    Args:
        text: Text to translate
        source: Source language code (or 'auto')
        target: Target language code
    
    Returns:
        Translated text or error message
    """
    try:
        if not text or not text.strip():
            return "الرجاء إدخال نص للترجمة / Please enter text to translate"
        
        if source == "auto":
            translator = GoogleTranslator(source='auto', target=target)
        else:
            translator = GoogleTranslator(source=source, target=target)
        
        result = translator.translate(text)
        return result
    
    except Exception as e:
        return f"خطأ في الترجمة / Translation Error: {str(e)}"