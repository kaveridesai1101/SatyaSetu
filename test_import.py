
try:
    print("Importing config...")
    import config
    print("Config imported.")

    print("Importing logger...")
    from src.utils.logger import get_logger
    print("Logger imported.")

    print("Importing spacy...")
    import spacy
    print("Spacy imported. Version:", spacy.__version__)

    print("Importing TextPreprocessor...")
    from src.preprocessing import TextPreprocessor
    print("TextPreprocessor imported.")

except Exception as e:
    import traceback
    traceback.print_exc()
