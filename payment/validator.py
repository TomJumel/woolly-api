from sales.models import OrderValidationException, Order, OrderLine, OrderStatus
from django.utils import timezone
from typing import List, Sequence
from collections import namedtuple


class OrderValidator:
	"""
	Object that can validate an order
	"""

	def __init__(self, order: Order, raise_on_error: bool=True):
		# TODO : Optimize
		# self.order = Order.objects.select_related('sale', 'owner') \
		# 					.prefetch_related('orderlines', 'orderlines__item', 'sale__items', 'owner__orders') \
		# 					.get(pk=order.pk)
		# TODO Check if oauth not needed or find oauth in cache
		self.order = order
		self.owner = self.order.owner.get_with_api_data()
		self.sale = self.order.sale

		self.raise_on_error = raise_on_error
		self.now = timezone.now()
		self.errors = []
		self.checked = False

	def validate(self):
		"""
		Vérifie la validité d'un order
		"""
		self.checked = True
		self._check_sale()
		self._check_order()
		self._check_quantities()

	@property
	def is_valid(self) -> bool:
		if not self.checked:
			raise OrderValidationException(
				"La commande doit être vérifiée avant d'être validée",
				'check_order_before_is_valid',
				status_code=500)

		return len(self.errors) == 0

	def get_errors(self) -> List[str]:
		return self.errors

	def _add_error(self, message: str, code: str=None):
		"""
		Raise or add a new error
		"""
		self.errors.append(message)
		if self.raise_on_error:
			raise OrderValidationException(message, code)

	# ===============================================
	# 			Check functions
	# ===============================================

	def _check_sale(self):
		"""
		Check general settings on the sale
		"""
		# Check if sale is active
		if not self.sale.is_active:
			self._add_error("La vente n'est pas disponible.")

		# Check dates
		if self.now < self.sale.begin_at:
			self._add_error("La vente n'a pas encore commencé.")
		if self.now > self.sale.end_at:
			self._add_error("La vente est terminée.")

	def _check_order(self):
		"""
		Check general settings on the order
		"""
		# Check if order is still buyable
		if self.order.status not in OrderStatus.BUYABLE_STATUS_LIST.value:
			self._add_error("Votre commande n'est pas payable.")

		# TODO Check if expired

		# Check if no previous ongoing order on the same sale
		user_prev_ongoing_orders = self.owner.orders.filter(
			status=OrderStatus.ONGOING.value,
			sale=self.sale.pk
		).exclude(pk=self.order.pk)
		if user_prev_ongoing_orders:
			self._add_error("Vous avez déjà une commande en cours pour cette vente.")

		# Check if user can buy items
		for orderline in self.order.orderlines.prefetch_related('item', 'item__usertype').all():
			if not orderline.item.usertype.check_user(self.owner):
				self._add_error(f"L'article {orderline.item.name} est réservé à {orderline.item.usertype.name}")

	def _check_quantities(self):
		"""
		Fetch, Process and Verify Quantities
		"""
		# ======= Part I - Fetch resources
		# TODO : optimize (orderlinefield.orderlineitem.orderline.order.sale.association)

		# sale_items = self.sale.items.prefetch_related('group').all()
		order_orderlines = self.order.orderlines.prefetch_related('item').all()
		# All orders which book items except the one we are processing
		sale_orderlines = OrderLine.objects \
							.filter(order__sale__pk=self.sale.pk, order__status__in=OrderStatus.BOOKING_LIST.value) \
							.exclude(order__pk=self.order.pk) \
							.prefetch_related('item', 'item__group')
		# Orders that the user already booked
		user_orderlines = sale_orderlines.filter(order__owner__pk=self.owner.pk)

		# ======= Part II - Process quantities

		Quantity = namedtuple('Quantity', ['total', 'per_item', 'per_group'])

		def build_quantity(orderlines: Sequence[OrderLine]) -> Quantity:
			"""
			Helper to build total, per item and per group quantities
			"""
			count, per_item, per_group = 0, {}, {}
			for orderline in orderlines:
				count += orderline.quantity
				per_item[orderline.item] = per_item.get(orderline.item, 0) + orderline.quantity
				if orderline.item.group:
					per_group[orderline.item.group] = per_group.get(orderline.item.group, 0) + orderline.quantity

			return Quantity._make([count, per_item, per_group])

		# Quantity per item and Total quantity bought in the order
		order_qt = build_quantity(order_orderlines)
		sale_qt  = build_quantity(sale_orderlines)
		user_qt  = build_quantity(user_orderlines)

		# ======= Part III - Verification

		def is_quantity(quantity) -> bool:
			return type(quantity) is int and quantity > 0

		# III.1 - Sale level verification

		if order_qt.total <= 0:
			self._add_error("Vous devez avoir un nombre d'items commandés strictement positif.")

		# Check max item quantity for the sale (ie. enough items left)
		if is_quantity(self.sale.max_item_quantity) and sale_qt.total + order_qt.total > self.sale.max_item_quantity:
			self._add_error("Il ne reste pas assez d'articles pour cette vente.")

		# III.2 - Item level verification
		for item, qt in order_qt.per_item.items():
			# Check quantity per item
			if is_quantity(item.quantity) and sale_qt.per_item.get(item, 0) + qt > item.quantity:
				self._add_error(f"Il ne reste pas assez de {item.name}.")

			# Check max_per_user per item
			if is_quantity(item.max_per_user) and user_qt.per_item.get(item, 0) + qt > item.max_per_user:
				self._add_error(f"Vous ne pouvez pas prendre plus de {item.max_per_user} {item.name} par utilisateur.")

		# III.3 - ItemGroup level verification
		for group, qt in order_qt.per_group.items():
			# Check quantity per group
			if is_quantity(group.quantity) and sale_qt.per_group.get(group, 0) + qt > group.quantity:
				self._add_error(f"Il ne reste pas assez de {group.name}.")

			# Check max_per_user per group
			if is_quantity(group.max_per_user) and user_qt.per_group.get(group, 0) + qt > group.max_per_user:
				self._add_error(f"Vous ne pouvez pas prendre plus de {group.max_per_user} {group.name} par utilisateur.")
