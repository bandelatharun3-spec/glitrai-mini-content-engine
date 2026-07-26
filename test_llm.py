from llm import generate_image_prompt

try:
    result = generate_image_prompt(
        "Florentine Wooden Salad Bowl",
        "A match made in summer - salads and wooden bowls. Handpainted on mango wood, this compact salad bowl serves a supper for two."
    )
    print(result)
except Exception as exc:
    print(f"LLM request failed: {exc}")