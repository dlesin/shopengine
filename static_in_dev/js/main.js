// cart scripts
$(document).ready(function () {
    $('.remove-from-cart').on('click', function (e) {
        e.preventDefault();
        product_slug = $(this).attr('data-slug');
        item_product_id = $(this).attr('data-id');
        data = {
            product_slug: product_slug
        };
        $.ajax({
            type: 'GET',
            url: '/remove_from_cart/',
            data: data,
            success: function (data) {
                $('#cart-count').html(data.cart_total);
                //$('.cart-item-' + item_product_id).css('display', 'none')
                $('.cart-item-' + item_product_id).remove();
                $('#cart-total-price').html('<strong>' + parseFloat(data.cart_total_price).toFixed(2) + ' руб.' + '</strong>');
                if (parseInt(data.cart_total) === 0) {
                    //$('.my-cart').css('display', 'none')
                    $('.my-cart').remove();
                    $('.cart-empty').html('<h3 class="text-center">Ваша корзина пуста</h3>')
                }
            }
        })
    })
});
$(document).ready(function () {
    $('#cart-item-qty').on('click', function (e) {
        qty = $(this).val();
        item_id = $(this).attr('data-id');
        data = {
            qty: qty,
            item_id: item_id
        };
        $.ajax({
            type: 'GET',
            url: '/change_item_qty/',
            data: data,
            success: function (data) {
                $('#cart-item-total-' + item_id).html('<strong>' + parseFloat(data.item_total).toFixed(2) + ' руб.' + '</strong>');
                $('#cart-total-price').html('<strong>' + parseFloat(data.cart_total_price).toFixed(2) + ' руб.' + '</strong>')
            }
        })
    })
});
$(document).ready(function () {
    $('#cart-item-qty').on('input keyup', function (e) {
        e.preventDefault();
        qty = $(this).val();
        if (qty <= 5 && qty != '') {        
            item_id = $(this).attr('data-id');
            data = {
                qty: qty,
                item_id: item_id
            };
            $.ajax({
                type: 'GET',
                url: '/change_item_qty/',
                data: data,
                success: function (data) {
                    $('#cart-item-total-' + item_id).html('<strong>' + parseFloat(data.item_total).toFixed(2) + ' руб.' + '</strong>');
                    $('#cart-total-price').html('<strong>' + parseFloat(data.cart_total_price).toFixed(2) + ' руб.' + '</strong>')
                }
            })
        }
    })
});
// product scripts
$(document).ready(function () {
    $('#add-to-cart').on('click', function (e) {
        e.preventDefault();
        product_slug = $(this).attr('data-slug');
        data = {
            product_slug: product_slug
        };
        $.ajax({
            type: 'GET',
            url: '/add_to_cart/',
            data: data,
            success: function (data) {
                $('#cart-count').html(data.cart_total);
                $('#add-to-cart').remove();
                $('#button').html('<a href="/cart/" id="add-to-cart-order">' + '<button class="btn btn-success">' + 'Оформить' + '</button>' + '</a>')
            }
        })
    })
});
// order scripts
$(document).ready(function () {
    //$('#div_id_address').css('display', 'none');
    $('#id_buying_type').on('click', function () {
        buying_type = $(this).val()
        if(buying_type === 'delivery') {
            $('#id_address').css('display', 'block');
        }else {
            $('#id_address').css('display', 'none');
        }
    })
});
