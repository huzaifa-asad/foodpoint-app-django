from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from datetime import datetime
from .models import Dish, Reservation as ReservationModel, Order as OrderModel
from django.db.models import Q


def home(request):
    dishes = Dish.objects.filter(is_featured=True).order_by('-updated_at')[:8]
    return render(request, 'core/home.html', {"dishes": dishes})


def reservation(request):
    context = {"submitted": False, "errors": {}, "data": {}}

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        phone = request.POST.get("phone", "").strip()
        date = request.POST.get("date", "").strip()
        time = request.POST.get("time", "").strip()
        guests = request.POST.get("guests", "").strip()
        email = request.POST.get("email", "").strip()
        notes = request.POST.get("notes", "").strip()

        errors = {}
        if not name:
            errors["name"] = "Name is required."
        if not phone:
            errors["phone"] = "Phone is required."
        if not date:
            errors["date"] = "Date is required."
        if not time:
            errors["time"] = "Time is required."
        if not guests or not guests.isdigit() or int(guests) <= 0:
            errors["guests"] = "Guests must be a positive number."

        if errors:
            context["errors"] = errors
            context["data"] = {
                "name": name,
                "phone": phone,
                "date": date,
                "time": time,
                "guests": guests,
                "email": email,
                "notes": notes,
            }
        else:
            # Parse date/time
            try:
                date_obj = datetime.strptime(date, "%Y-%m-%d").date()
            except Exception:
                date_obj = None
            try:
                time_obj = datetime.strptime(time, "%H:%M").time()
            except Exception:
                time_obj = None
            # Save reservation
            ReservationModel.objects.create(
                name=name,
                phone=phone,
                email=email,
                date=date_obj,
                time=time_obj,
                guests=int(guests),
                notes=notes,
            )
            context["submitted"] = True
            context["data"] = {
                "name": name,
                "phone": phone,
                "date": date,
                "time": time,
                "guests": int(guests),
                "email": email,
                "notes": notes,
            }

    return render(request, 'core/reservation.html', context)

def menu(request):
    q = request.GET.get("q", "").strip()
    qs = Dish.objects.all().order_by('-updated_at')
    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(description__icontains=q))
    context = {"q": q, "results": list(qs), "count": qs.count()}
    return render(request, 'core/menu.html', context)

def tracking(request):
    # Sample orders; replace with DB lookup later
    orders = [
        {
            "code": "FP1234",
            "phone": "+1 (000) 000-0000",
            "status": "Out for delivery",
            "steps": [
                "Order placed",
                "Preparing",
                "Ready for pickup",
                "Out for delivery",
                "Delivered",
            ],
            "current_step": 3,  # zero-based index
            "eta": "15–20 min",
            "items": ["Paneer Tikka x1", "Butter Paneer x1"],
            "total": 21.48,
            "placed_at": "2025-08-31 18:45",
        },
        {
            "code": "FP5678",
            "phone": "+1 (000) 111-2222",
            "status": "Preparing",
            "steps": [
                "Order placed",
                "Preparing",
                "Ready for pickup",
                "Out for delivery",
                "Delivered",
            ],
            "current_step": 1,
            "eta": "30–35 min",
            "items": ["Paneer Masala x2"],
            "total": 20.98,
            "placed_at": "2025-08-31 19:05",
        },
    ]

    q = request.GET.get("order", "").strip()
    found = None
    if q:
        q_lower = q.lower()
        for o in orders:
            if o["code"].lower() == q_lower or o["phone"].lower() == q_lower:
                found = o
                break

    context = {"q": q, "order": found, "not_found": bool(q and not found)}
    return render(request, 'core/tracking.html', context)

def contact(request):
    return render(request, 'core/contact.html')

# --- Cart (session-based) ---
def _get_cart(session):
    cart = session.get('cart')
    if not isinstance(cart, dict):
        cart = {}
    return cart


def cart_add(request, dish_id: int):
    dish = get_object_or_404(Dish, id=dish_id)
    cart = _get_cart(request.session)
    qty = int(request.GET.get('qty', '1') or '1')
    cart[str(dish.id)] = cart.get(str(dish.id), 0) + max(1, qty)
    request.session['cart'] = cart
    request.session.modified = True
    return redirect(request.GET.get('next') or 'cart')


def cart_remove(request, dish_id: int):
    cart = _get_cart(request.session)
    cart.pop(str(dish_id), None)
    request.session['cart'] = cart
    request.session.modified = True
    return redirect('cart')


def cart_detail(request):
    cart = _get_cart(request.session)
    item_ids = [int(i) for i in cart.keys()]
    dishes = Dish.objects.filter(id__in=item_ids)
    items = []
    total = 0.0
    for d in dishes:
        q = int(cart.get(str(d.id), 0))
        line_total = float(d.price) * q
        total += line_total
        items.append({
            'dish': d,
            'qty': q,
            'line_total': line_total,
        })
    context = {'items': items, 'total': total}
    return render(request, 'core/cart.html', context)

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404
from .models import Dish

def _get_cart(session):
    return session.setdefault('cart', {})  # { "dish_id": qty }

def _cart_totals(session):
    cart = session.get('cart', {})
    total = 0
    count = 0
    for sid, qty in cart.items():
        dish = Dish.objects.get(pk=int(sid))
        count += int(qty)
        total += float(dish.price) * int(qty)
    return count, total

@require_POST
def cart_increase(request, dish_id):
    cart = _get_cart(request.session)
    key = str(dish_id)
    cart[key] = int(cart.get(key, 0)) + 1
    request.session.modified = True

    dish = get_object_or_404(Dish, pk=dish_id)
    count, total = _cart_totals(request.session)
    return JsonResponse({
        "qty": cart[key],
        "line_total": float(dish.price) * int(cart[key]),
        "cart": {"items": count, "total": total}
    })

@require_POST
def cart_decrease(request, dish_id):
    cart = _get_cart(request.session)
    key = str(dish_id)
    cart[key] = max(1, int(cart.get(key, 1)) - 1)
    request.session.modified = True

    dish = get_object_or_404(Dish, pk=dish_id)
    count, total = _cart_totals(request.session)
    return JsonResponse({
        "qty": cart[key],
        "line_total": float(dish.price) * int(cart[key]),
        "cart": {"items": count, "total": total}
    })