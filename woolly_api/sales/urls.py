from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns

from .views import SaleViewSet, AssociationViewSet, ItemViewSet, ItemSpecificationsViewSet
from .views import AssociationRelationshipView, SaleRelationshipView
from .views import ItemSpecificationsRelationshipView, OrderRelationshipView
from .views import AssociationRelationshipView, ItemRelationshipView, api_root
from .views import OrderViewSet, OrderLineViewSet, OrderLineRelationshipView
from .views import OrderLineItemViewSet
from authentication.views import WoollyUserTypeViewSet

usertype_list = WoollyUserTypeViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
usertype_detail = WoollyUserTypeViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

sale_list = SaleViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
sale_detail = SaleViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

association_list = AssociationViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
association_detail = AssociationViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

item_list = ItemViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
item_detail = ItemViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

itemSpecifications_list = ItemSpecificationsViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
itemSpecifications_detail = ItemSpecificationsViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

order_list = OrderViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
order_detail = OrderViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

orderline_list = OrderLineViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
orderline_detail = OrderLineViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

orderlineitem_list = OrderLineItemViewSet.as_view({
    'get': 'list',
    'post': 'create'
})
orderlineitem_detail = OrderLineItemViewSet.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})


urlpatterns = [
    # Root
    url(r'^$', api_root),

    # Associations
    url(r'^assos/$', association_list, name='association-list'),
    url(r'^assos/(?P<pk>[0-9]+)/$',
        association_detail, name='association-detail'),

    # Sales
    url(r'^sales/$', sale_list, name='sale-list'),
    url(r'^sales/(?P<pk>[0-9]+)$', sale_detail, name='sale-detail'),
    url(r'^assos/(?P<association_pk>[0-9]+)/sales/$',
        sale_list, name='sale-list'),
    url(r'^assos/(?P<association_pk>[0-9]+)/sales/(?P<pk>[0-9]+)$',
        sale_detail, name='sale-detail'),

    # Items
    url(r'^items/$', item_list, name='item-list'),
    url(r'^items/(?P<pk>[0-9]+)$', item_detail, name='item-detail'),
    url(r'^sales/(?P<sale_pk>[0-9]+)/items/$', item_list, name='item-list'),
    url(r'^assos/(?P<association_pk>[0-9]+)/sales/(?P<sale_pk>[0-9]+)/items/$',
        item_list, name='item-list'),
    url(r'^assos/(?P<association_pk>[0-9]+)/sales/(?P<sale_pk>[0-9]+)/items/(?P<pk>[0-9]+)$',
        item_detail, name='item-detail'),

    # Spec
    url(r'^specs/$', itemSpecifications_list, name='itemSpecification-list'),
    url(r'^specs/(?P<pk>[0-9]+)$', itemSpecifications_detail,
        name='itemSpecification-detail'),
    url(r'^items/(?P<item_pk>[0-9]+)/spec/$',
        itemSpecifications_list, name='itemSpecification-list'),
    url(r'^spec/(?P<itemspec_pk>[0-9]+)/utype/$',
        usertype_list, name='usertype-list'),

    # User Type
    url(r'^utype/$',
        usertype_list, name='usertype-list'),
    url(r'^utype/(?P<pk>[0-9]+)/$',
        usertype_detail, name='usertype-detail'),

    # Orders
    url(r'^orders/$',
        order_list, name='order-list'),
    url(r'^orders/(?P<pk>[0-9]+)/$',
        order_detail, name='order-detail'),
    url(r'^orders/(?P<order_pk>[0-9]+)/lines/$',
        orderline_list, name='orderline-list'),
    url(r'^orders/(?P<order_pk>[0-9]+)/lines/(?P<pk>[0-9]+)$',
        orderline_detail, name='orderline-detail'),
    url(r'^orderlines/(?P<orderline_pk>[0-9]+)/items/$',
        orderlineitem_list, name='orderlineitem-list'),
    url(r'^orderlines/(?P<orderline_pk>[0-9]+)/lines/(?P<pk>[0-9]+)$',
        orderlineitem_detail, name='orderlineitem-detail'),
    # url(r'^orders/(?P<order_pk>[0-9]+)/lines/(?P<orderline_pk>[0-9]+)/items$',
    #    item_list, name='item-list'),
    # url(r'^orders/(?P<order_pk>[0-9]+)/lines/(?P<orderline_pk>[0-9]+)/items/(?P<pk>[0-9]+)$',
    #    item_detail, name='item-detail'),

    # Relationships views for the related links
    url(
        regex=r'^assos/(?P<pk>[^/.]+)/relationships/(?P<related_field>[^/.]+)$',
        view=AssociationRelationshipView.as_view(),
        name='maison-relationships'
    ),
    url(
        regex=r'^assos/(?P<pk>[^/.]+)/relationships/(?P<related_field>[^/.]+)$',
        view=AssociationRelationshipView.as_view(),
        name='association-relationships'
    ),
    url(
        regex=r'^sales/(?P<pk>[^/.]+)/relationships/(?P<related_field>[^/.]+)$',
        view=SaleRelationshipView.as_view(),
        name='sale-relationships'
    ),
    url(
        regex=r'^items/(?P<pk>[^/.]+)/relationships/(?P<related_field>[^/.]+)$',
        view=ItemRelationshipView.as_view(),
        name='item-relationships'
    ),
    url(
        regex=r'^specs/(?P<pk>[^/.]+)/relationships/(?P<related_field>[^/.]+)$',
        view=ItemSpecificationsRelationshipView.as_view(),
        name='itemSpecification-relationships'
    ),
    url(
        regex=r'^orders/(?P<pk>[^/.]+)/relationships/(?P<related_field>[^/.]+)$',
        view=OrderRelationshipView.as_view(),
        name='order-relationships'
    ),
    url(
        regex=r'^orderlines/(?P<pk>[^/.]+)/relationships/(?P<related_field>[^/.]+)$',
        view=OrderLineRelationshipView.as_view(),
        name='orderline-relationships'
    )
]
