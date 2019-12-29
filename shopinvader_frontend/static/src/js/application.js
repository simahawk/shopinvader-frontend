// TODO: see application.orig.tocherrypick.js for the complete original file
$(document).ready(function () {
  
  // $(document).on('ShopinvaderForm:after-error',
  //   function (element)
  //   {
  //     $('.main-loader').addClass('d-none');
  //     $('#generic-error-message').modal('show');
  //   }
  // );

  // $(document).on('ShopinvaderForm:before-submit',
  //   function (element)
  //   {
  //     $('.main-loader').removeClass('d-none');
  //   }
  // );

  // $(document).on('ShopinvaderForm:after-submit',
  //   function (event, element)
  //   {
  //     $('.main-loader').addClass('d-none');
  //     var new_document = $('<div></div>').append($.parseHTML(element.ajaxpage));
  //     if($(element.target).attr('action') == '/invader/cart/add_item') {
  //       main_modal.show(
  //         new_document.find('#product-modal-add .title').html(),
  //         new_document.find('#product-modal-add .content').html(),
  //         ''
  //       );
  //     }
  //   }
  // );

  $('body').on('click',".cart-items .delete",
    function() {
      $('form#'+$(this).data('form-submit')).submit();
    }
  );

  $('body').on('change',"[data-autosubmit]",
    function() {
      $(this).parents('form').submit();
    }
  );
  $('[data-toggle=display-hover]').hover(
    function() {
      $($(this).attr('data-target')).css('display', 'block');
    },
    function() {
      $($(this).attr('data-target')).css('display', 'none');
    }
  );
  $('[data-toggle=display-hover]').hover(
    function() {
      $($(this).attr('data-target')).css('display', 'block');
    },
    function() {
      $($(this).attr('data-target')).css('display', 'none');
    }
  );
 
  $('body').on('change', '.product-qty input',
    function(event) {
      var max_value = 100;
      var min_value = 1;
      /*Set custom max value*/
      if($(this).attr('max')) {
        max_value = $(this).attr('max');
      }
      /*Set custom min value*/
      if($(this).attr('min')) {
        min_value = $(this).attr('min');
      }
      var current_value = parseInt($(this).val())

      if(current_value > max_value) {
        current_value = max_value;
      }
      if(current_value < min_value) {
        current_value = min_value;
      }
      if(isNaN(current_value)) {
        current_value = min_value;
      }
      $(this).val(current_value);
      if($(this).parents('.cart-line-qty').length > 0) {
        /*Input in cart lines*/
        $(this).parents('form').submit();
      }
    }
  );

  $('body').on('click', '.product-qty [data-type]',
    function(event) {
      var input_qty = $(event.currentTarget).parent('.input-group').find('input.form-control');

      if(input_qty.length > 0) {
        var qty = input_qty.val();
        if($(this).attr('data-type') == 'minus') {
          qty--;
          if(qty < 1) {
            qty = 1;
          }
        }
        else {
          qty++;
        }
        input_qty.val(qty);
        input_qty.trigger('change');
      }
    }
  );

  // $('body').on('submit', '#cart_address', function(event) {
  //   event.preventDefault();
  //   if($(this).find('#use_specific_address:checked').length == 0) {
  //     var shipping_addresss_id = $('input.input-shipping-address:checked').val();
  //     $('input.input-invoicing-address[value='+shipping_addresss_id+']').prop('checked', true);
  //   }
  //   $(this).get(0).submit();
  // });

  /*common event*/
  $('body').on('click', '[data-link]',
    function(){
      window.location=$(this).attr('data-link');
    }
  );

  // $('body').on('click', '[data-scrollto]',
  //   function(){
  //     $('html, body').animate({
  //         scrollTop: $($(this).data('scrollto')).offset().top - $('.navbar-fixed-top').height()
  //     }, 1500);
  //   }
  // );

});
