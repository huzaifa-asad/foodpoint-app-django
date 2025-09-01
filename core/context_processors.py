from typing import Dict, Any


def cart(request) -> Dict[str, Any]:
    data = request.session.get("cart", {})
    try:
        count = sum(int(q) for q in data.values())
    except Exception:
        count = 0
    return {"cart_count": count}
