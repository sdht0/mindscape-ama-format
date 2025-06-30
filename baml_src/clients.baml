// Learn more about clients at https://docs.boundaryml.com/docs/snippets/clients/overview

client<llm> OllamaClient {
  provider "openai-generic"
  options {
    model "qwen3:8b"
    base_url "http://192.168.2.95:11434/v1"
  }
}

retry_policy Exponential {
  max_retries 2
  // Strategy is optional
  strategy {
    type exponential_backoff
    delay_ms 300
    multiplier 1.5
    max_delay_ms 10000
  }
}
