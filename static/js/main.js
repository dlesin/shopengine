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
		          if(parseInt(data.cart_total) === 0){
                  //$('.my-cart').css('display', 'none')
				          $('.my-cart').remove();
				          $('.cart-empty').html('<h3 class="text-center">Ваша корзина пуста</h3>')
              }
          }
      })
  })
  });
  $(document).ready(function () {
    $('.cart-item-qty').on('click', function(e){
      qty = $(this).val();
      item_id = $(this).attr('data-id');
      data = {
        qty: qty,
        item_id: item_id
      };
      $.ajax({
              type: 'GET',
              url: '{% url "change_item_qty_url" %}',
              data: data,
              success: function (data) {
                $('#cart-item-total-'+item_id).html('<strong>' + parseFloat(data.item_total).toFixed(2) + ' руб.' + '</strong>');
                $('#cart-total-price').html('<strong>' + parseFloat(data.cart_total_price).toFixed(2) + ' руб.' + '</strong>')
              }
          })
    })
  })