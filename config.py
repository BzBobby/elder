# config.py

# ✅ LLM API 接口地址和密钥
API_KEY    = "sk-gafqdvdddiipkmguddwjftxlvktrasobarnqloqwrbisrthl"
API_URL    = "https://api.siliconflow.cn/v1/chat/completions"

# ✅ 模型名称（与你的 API 服务匹配）
MODEL = "deepseek-ai/DeepSeek-V3" 

# ✅ 对话历史长度限制（每轮最多取多少轮历史上下文）
MAX_HISTORY = 10

# ✅ 最大回复 token 长度（影响生成长度）
MAX_TOKENS = 1024

# ✅ 是否启用 TTS（备用参数，如果想关掉语音播报）
ENABLE_TTS = True
