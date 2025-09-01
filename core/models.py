from django.db import models


class TimeStampedModel(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True


class Dish(TimeStampedModel):
	name = models.CharField(max_length=120)
	description = models.TextField(blank=True)
	price = models.DecimalField(max_digits=7, decimal_places=2)
	image = models.ImageField(upload_to='dishes/', blank=True, null=True)
	static_image = models.CharField(max_length=255, blank=True, help_text="Optional static image path, e.g. core/images/paneer.png")
	is_featured = models.BooleanField(default=True)

	def __str__(self) -> str:
		return self.name


class Reservation(TimeStampedModel):
	name = models.CharField(max_length=120)
	phone = models.CharField(max_length=40)
	email = models.EmailField(blank=True)
	date = models.DateField()
	time = models.TimeField()
	guests = models.PositiveIntegerField(default=1)
	notes = models.TextField(blank=True)
	STATUS_CHOICES = [
		("new", "New"),
		("confirmed", "Confirmed"),
		("seated", "Seated"),
		("completed", "Completed"),
		("cancelled", "Cancelled"),
	]
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new")

	def __str__(self) -> str:
		return f"Reservation for {self.name} on {self.date} {self.time}"


class Order(TimeStampedModel):
	STATUS_CHOICES = [
		("placed", "Order placed"),
		("preparing", "Preparing"),
		("ready", "Ready for pickup"),
		("out", "Out for delivery"),
		("delivered", "Delivered"),
	]
	code = models.CharField(max_length=20, unique=True)
	phone = models.CharField(max_length=40)
	status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="placed")
	eta = models.CharField(max_length=40, blank=True)
	items_json = models.TextField(blank=True, help_text="JSON array of item strings")
	total = models.DecimalField(max_digits=8, decimal_places=2, default=0)
	placed_at = models.DateTimeField()

	def __str__(self) -> str:
		return f"{self.code} - {self.get_status_display()}"
