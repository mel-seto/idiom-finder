

# 🀄 Chinese Idiom Finder  

An interactive app to discover and learn **Chinese idioms (成语, 俗语, 谚语)**.  
Given a situation, the app suggests a relevant idiom, provides **pinyin**, a **literal English translation**, and a **concise explanation**.  

---

## ✨ Features  
- 🔍 **Idiom search** using an LLM with Cerebras inference.  
- ✅ **Idiom verification** using:  
  - [ChID dataset](https://arxiv.org/abs/1906.01265) (Chinese Idiom Dataset)  
  - CC-CEDICT (open Chinese–English dictionary)  
  - Wiktionary 

---

## 🚀 How It Works  
1. User inputs a situation (e.g. *“When you stay calm under pressure”*).  
2. The LLM generates an idiom suggestion.  
3. The idiom is verified against datasets/dictionaries.  
4. Output includes:  
   - Idiom in Chinese  
   - Pinyin  
   - Literal translation  
   - Concise explanation  

---

## 🛠️ Tech Stack  
- [Gradio](https://www.gradio.app/) (frontend)  
- Hugging Face Spaces (deployment)  
- OpenAI-compatible LLM API  
- Python (requests, pypinyin, etc.)  

---

## 🖥️ Local Development  

Clone the repo and run locally:  

```bash
git clone https://huggingface.co/spaces/chinese-enthusiasts/idiom-finder
cd idiom-finder
pip install -r requirements.txt
python app.py


# HuggingFace setup
---

title: Chinese Idiom Finder
emoji: 💬
colorFrom: yellow
colorTo: purple
sdk: gradio
sdk_version: 5.42.0
app_file: src/app.py
pinned: false
hf_oauth: true
hf_oauth_scopes:
 - inference-api
---