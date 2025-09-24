#!/usr/bin/env python3
"""
Debug tokenization issue
"""

import sys
import traceback

try:
    from indictrans2_service import IndicTrans2Service
    service = IndicTrans2Service()
    if service.model_loaded:
        print('Model loaded successfully')
        text = 'potato'
        processed = service._preprocess_batch([text], src_lang='eng_Latn', tgt_lang='hin_Deva')
        print(f'Processed text: {processed[0]}')

        # Try tokenization
        inputs = service.tokenizer(
            processed[0],
            return_tensors="pt",
            padding=True,
            truncation=True,
            max_length=256
        )
        print(f'Tokenization successful')
        print(f'Input keys: {list(inputs.keys())}')
        print(f'Input IDs shape: {inputs["input_ids"].shape}')
        print(f'Input IDs: {inputs["input_ids"].tolist()}')

        # Try generation
        import torch
        with torch.no_grad():
            outputs = service.model.generate(
                inputs['input_ids'],
                attention_mask=inputs.get('attention_mask'),
                num_beams=5,
                max_length=256,
                min_length=0,
                do_sample=False,
                use_cache=False,
                pad_token_id=service.tokenizer.pad_token_id,
                eos_token_id=service.tokenizer.eos_token_id,
                bos_token_id=service.tokenizer.bos_token_id
            )
            print(f'Generation successful')
            print(f'Output shape: {outputs.shape}')

            # Decode
            raw_translation = service.tokenizer.decode(outputs[0], skip_special_tokens=True)
            print(f'Raw translation: {raw_translation}')

    else:
        print('Model not loaded')

except Exception as e:
    print(f"Error: {e}")
    traceback.print_exc()