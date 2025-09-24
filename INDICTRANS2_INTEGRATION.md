# VaaniMitra - IndicTrans2 Integration

## Overview
VaaniMitra now includes automated translation to all Indian languages using the IndicTrans2 model by AI4Bharat. This eliminates the need for manual translation and provides comprehensive multilingual support.

## Features Added

### 🚀 IndicTrans2 Integration
- **Automated Translation**: Translate content to 20+ Indian languages automatically
- **High Quality**: Uses state-of-the-art IndicTrans2 model for accurate translations
- **Real-time**: Dynamic language switching without page reloads
- **Comprehensive**: Supports Hindi, Tamil, Bengali, Gujarati, Kannada, Malayalam, Marathi, Telugu, Urdu, and more

### 🗃️ Enhanced Database Models
- **MultilingualVocabulary**: Store vocabulary with translations for all languages
- **UserLanguagePreference**: Track user language preferences and learning goals
- **Bulk Operations**: Efficient batch translation and storage

### 🌐 API Endpoints
- `GET /api/languages` - Get supported languages
- `POST /api/translate` - Translate text to any Indian language
- `GET /api/vocabulary/<category>` - Get vocabulary in user's preferred language
- `POST /api/user/language-preference` - Set user language preferences
- `GET /api/vocabulary/search` - Search vocabulary across languages

### 🎨 Frontend Enhancements
- **Language Selector**: Dropdown to switch between Indian languages
- **Dynamic Content**: Real-time content translation
- **Smooth Transitions**: Visual feedback during language switching
- **Persistent Preferences**: Remembers user's language choice

## Supported Languages

| Language | Script | Code |
|----------|--------|------|
| Hindi | देवनागरी | hin_Deva |
| Bengali | বাংলা | ben_Beng |
| Gujarati | ગુજરાતી | guj_Gujr |
| Kannada | ಕನ್ನಡ | kan_Knda |
| Malayalam | മലയാളം | mal_Mlym |
| Marathi | मराठी | mar_Deva |
| Oriya | ଓଡ଼ିଆ | ori_Orya |
| Punjabi | ਪੰਜਾਬੀ | pan_Guru |
| Tamil | தமிழ் | tam_Taml |
| Telugu | తెలుగు | tel_Telu |
| Urdu | اردو | urd_Arab |
| Assamese | অসমীয়া | asm_Beng |
| Nepali | नेपाली | npi_Deva |
| Sanskrit | संस्कृत | san_Deva |

## Installation

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Download IndicTrans2 Model
The model will be automatically downloaded on first use (requires internet connection).

### 3. Configure Environment
```bash
# Set up MongoDB connection
export MONGODB_URI="mongodb://localhost:27017/"
export DATABASE_NAME="vaanimitra_db"
```

### 4. Initialize Vocabulary
```bash
# Populate vocabulary with translations
curl -X POST http://localhost:5000/api/admin/populate-vocabulary
```

## Usage

### Basic Translation
```python
from translation_service import get_translator

translator = get_translator()
hindi_text = translator.translate_text("Hello, how are you?", "hindi")
print(hindi_text)  # नमस्ते, आप कैसे हैं?
```

### Batch Translation
```python
texts = ["Dog", "Cat", "Elephant"]
tamil_translations = translator.translate_batch(texts, "tamil")
# ['நாய்', 'பூனை', 'யானை']
```

### API Usage
```javascript
// Change language preference
fetch('/api/user/language-preference', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({preferred_language: 'hindi'})
});

// Get vocabulary in user's language
fetch('/api/vocabulary/animals?language=tamil')
    .then(response => response.json())
    .then(data => console.log(data.vocabulary));
```

## Performance Optimization

### GPU Support
- Automatically uses CUDA if available
- Falls back to CPU for compatibility
- Model loading is cached for subsequent requests

### Memory Management
- Lazy model loading (loads only when needed)
- Efficient batch processing
- Automatic cleanup of model resources

### Caching Strategy
- Translation results cached in database
- User preferences stored in session
- Vocabulary pre-computed for faster access

## Testing

### Quick Test
```bash
python test_translation.py
```

### Full Model Test
```bash
# Choose option 1 for full model test
python test_translation.py
```

### API Testing
```bash
# Test language support
curl http://localhost:5000/api/languages

# Test translation
curl -X POST http://localhost:5000/api/translate \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello World", "target_language": "hindi"}'
```

## Technical Architecture

### Translation Pipeline
1. **Input Processing**: Text preprocessing and language detection
2. **Model Inference**: IndicTrans2 model generates translations
3. **Post-processing**: Clean and format output text
4. **Caching**: Store results for future use

### Database Schema
```
multilingual_vocabulary: {
  category: String,
  key: String,
  english: String,
  translations: {
    hindi: String,
    tamil: String,
    // ... other languages
  }
}

user_language_preferences: {
  user_id: ObjectId,
  preferred_language: String,
  native_language: String,
  learning_languages: [String]
}
```

### API Response Format
```json
{
  "success": true,
  "original": "Hello",
  "translation": "नमस्ते",
  "target_language": "hindi"
}
```

## Troubleshooting

### Common Issues

1. **Model Loading Slow**
   - First-time download can take 5-10 minutes
   - Subsequent loads are much faster
   - Consider using GPU for better performance

2. **Translation Quality**
   - IndicTrans2 works best with complete sentences
   - Single words may have multiple valid translations
   - Context helps improve accuracy

3. **Memory Issues**
   - Model requires ~2GB RAM minimum
   - Use CPU version if GPU memory insufficient
   - Consider batch processing for large datasets

### Error Handling
- Graceful fallback to English if translation fails
- Automatic retry for network issues
- Comprehensive error logging

## Future Enhancements

### Planned Features
- [ ] Speech synthesis for all Indian languages
- [ ] Advanced grammar checking
- [ ] Cultural context annotations
- [ ] Dialect-specific translations
- [ ] Voice-to-voice translation

### Performance Improvements
- [ ] Model quantization for faster inference
- [ ] Redis caching for frequently used translations
- [ ] Load balancing for multiple model instances
- [ ] Asynchronous batch processing

## Contributing

### Adding New Languages
1. Update `supported_languages` mapping in `translation_service.py`
2. Add language display names in `translation_routes.py`
3. Update frontend language selector
4. Test translations and add to test suite

### Improving Translations
1. Contribute to IndicTrans2 training data
2. Report translation quality issues
3. Suggest domain-specific terminology
4. Help with post-processing rules

## License

This project uses IndicTrans2 under the MIT License. Please refer to the original model's license for commercial usage terms.

## Acknowledgments

- **AI4Bharat** for the excellent IndicTrans2 model
- **Hugging Face** for the transformers library
- **MongoDB** for flexible multilingual data storage
- **Flask** for the web framework

## Support

For issues related to:
- **IndicTrans2 Model**: [AI4Bharat GitHub](https://github.com/AI4Bharat/IndicTrans2)
- **VaaniMitra Integration**: Create an issue in this repository
- **General Usage**: Check the documentation or contact the development team

---

*VaaniMitra - Making Indian languages accessible through AI* 🚀