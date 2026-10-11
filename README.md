# n8n

## Telegram Summary

[ Manual Trigger ] 
       │
       ▼
[ Code: Check 24h Cooldown & Last Execution ]
       │
       ├────( Execution < 24 hours ) ───> [ End Execution / Halt ]
       │
       └────( Execution >= 24 hours )
               │
               ▼
      [ HTTP Request: Get Telegram Updates ]
               │
               ▼
      [ Code: Extract, Clean & Filter Messages ]
               │
               ▼
      [ Basic LLM Chain / Ollama Node (Qwen) ]
               │
               ▼
      [ Code: Split Long Summary into <32,768 Char Chunks ]
               │
               ▼
      [ Telegram Node: Send Summary Messages ]
               │
               ▼
      [ Code: Update & Save Last Execution Timestamp ]