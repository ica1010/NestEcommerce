$(document).ready(function (){
     $(".filter-checkbox , #price-filter-btn").on("click", function(){
         console.log("a checkbox have been clicked");
         let filter_object = {}
         let min_price = $('#max_price').attr('min')
         let max_price = $('#max_price').val()

         filter_object.min_price = min_price;
         filter_object.max_price = max_price;

         $(".filter-checkbox").each(function(){
            let filter_value = $(this).val()
            let filter_key = $(this).data('filter')
            
            filter_object[filter_key] = Array.from(document.querySelectorAll('input[data-filter='+ filter_key + ']:checked')).map(function(element){
            return element.value
        
        })
     })
     console.log(filter_object)
     
     $.ajax({
        url:'/filter-products',
        data: filter_object,
        dataType:'json',
        beforeSend: function(){
            console.log('sending data...');
        },
        success: function(response){
            console.log(response);
            console.log('data...');
            $("#filtered-product").html(response.data)
        }
     })
    })
    $('#max_price').on('blur', function(){
        let min_price = $(this).attr('min')
        let max_price = $(this).attr('max')
        let current_price = $(this).val()

         console.log('hhh',current_price);
         console.log(max_price);
         console.log(min_price);

        if(current_price < parseInt(min_price) || current_price > parseInt(max_price)){
            min_price = Math.round(min_price * 100) / 100
            max_price = Math.round(max_price * 100) / 100

            alert('price must between ' + min_price + ' and '+ max_price)
            $(this).val(min_price)
            $('#range').val(min_price)

            $(this).focus()
            return false
        }
     })
})

$(document).ready(function (){

    
$('.detail-qty').each(function () {
      qtyval = parseInt($(this).find('.qty-val').text(), 10);
      
        $('.qty-up').on('click', function (event) {
          event.preventDefault();
          qtyval = qtyval + 1;
          $(this).prev().text(qtyval);
     });
     $('.qty-down').on('click', function (event) {
         event.preventDefault();
         qtyval = qtyval - 1;
         if (qtyval > 1) {
             $(this).next().text(qtyval);
         } else {
             qtyval = 1;
             $(this).next().text(qtyval);
         }
     });
 });


$('.detail-qty').each(function () {
    let $this = $(this);
    let qtyval = parseInt($this.find('.qty-val').text(), 10);
    qtyval2 = parseInt($(this).find('.qtty').text(), 10);

    $this.find('.qty-up').on('click', function (event) {
        event.preventDefault();
        qtyval = qtyval + 1;
        $this.find('.qty-val').text(qtyval);
        console.log(qtyval)
        qtyval2=qtyval
        console.log(qtyval2)
    });

    $this.find('.qty-down').on('click', function (event) {
        event.preventDefault();
        qtyval = qtyval - 1;
        if (qtyval > 1) {
            $this.find('.qty-val').text(qtyval);
            qtyval2=qtyval
        } else {
            qtyval = 1;
            qtyval2=qtyval
            $this.find('.qty-val').text(qtyval);
        }
    });
});

$('.add-to-cart-btn').on('click', function(){
    // let quantity = $('#product-quantity').val()
    let this_val = $(this)
    let index = this_val.attr('data-index')

    // let quantity = $(qtyval + index).val()
    let quantity =1
    let product_color = $('.active .product-color-' + index ).val()
    let product_color_name = $('.active .product-color-name-' + index ).val()
    let product_size = $('.active .product-size-' + index ).val()
    let product_title = $('.product-title-' + index ).val()
    let product_vendor = $('.product-vendor-' + index ).val()

    let product_id = $('.product-id-' + index ).val()
    product_price = $('.current-product-price-' + index ).text()

    let product_pid = $('.product-pid-' + index ).val()
    let product_image = $('.product-image-' + index ).val()
    

    quantity= qtyval2
    console.log(quantity)
    console.log('color:', product_color)
    console.log('color:', product_color_name)
    console.log('size:', product_size)
    console.log(product_id)
    console.log(product_price)
    console.log(product_title)
    console.log(product_vendor)
    console.log(product_pid)
    console.log(product_image)
    console.log(index)
    console.log(this_val)

    let price = parseFloat(product_price);
    $.ajax({
        url:'/add-to-cart',
        data:{
            'id':product_id,
            'pid':product_pid,
            'qty':quantity,
            'size': product_size,
            'color_name': product_color_name,
            'color': product_color,
            'image':product_image,
            'title':product_title,
            'vendor':product_vendor,
            'price':price,
        },
        dataType:'json',
        beforeSend: function(){
            console.log('Adding Product to cart...');
        },
        success: function(response){
            this_val.html('<i class="fi-rs-check"></i>')
            console.log('added product to cart...');
            $(".cart-items-count").text(response.totalcartitems)
            console.log('ggg'+ response.totalcartitems)
            
        }
     })
    
})

$('.delete-product').on('click', function(){
    let product_id= $(this).attr('data-product')
    let this_val = $(this)

    console.log('prod id' + product_id);

    $.ajax({
        url:'/delete-from-cart',
        data:{
            'id':product_id,
        },
        dataType:'json',
        beforeSend: function(){
            this_val.hide()
        },
        success: function(response){
            this_val.show()
            $(".cart-items-count").text(response.totalcartitems)
            $("#cart-list").html(response.data)
            window.location.reload()
        }
     })
})

$('.update-product').on('click', function(){
    let product_id= $(this).attr('data-product')
    let this_val = $(this)
    let product_quantity = $('.product-qty-'+product_id).text()

    console.log('prod id:' + product_id);
    console.log('prod qty:' + product_quantity);

    $.ajax({
        url:'/update-cart',
        data:{
            'id':product_id,
            'qty':product_quantity,
        },
        dataType:'json',
        beforeSend: function(){
            this_val.hide()
        },
        success: function(response){
            this_val.show()
            $(".cart-items-count").text(response.totalcartitems)
            $("#cart-list").html(response.data)
            window.location.reload()
        }
    })
})

$(document).on('click', '.make-default-address', function(){
    let id = $(this).attr('data-address-id')
    let this_val = $(this)

    $.ajax({
        url:'/make-default-address',
        data:{
            'id':id
        },
        dataType:'json',
        success: function(response){
            console.log('address default');
            if (response.boolean == true){
                $('.check').hide()
                $(".action_btn").show()

                $('.check'+id).show()
                $('.button'+id).hide()
            }
        }
    })
})

$(document).on('click', '.data-to-wishlist', function(){
    let product_id = $(this).attr('data-product-item')
    let this_val = $(this)

    console.log('product id id', product_id);

    $.ajax({
        url:'/add-to-wishlist/',
        data:{
            'id':product_id
        },
        dataType:'json',
        beforeSend: function(){
            this_val.html('<i class="fa-solid fa-heart"></i>')
        },
        success: function(response){
            if (response.bool === true){
            console.log('added to whistlist ...');
            }
        }
    })
})
$(document).on('click', '.delete-wishlist-product', function(){
    let wishlist_id = $(this).attr('data-wishlist-product')
    let this_val = $(this)

    console.log(wishlist_id)
    $.ajax({
        url:'/remove-from-wishlist',
        data:{
            'id':wishlist_id
        },
        dataType:'json',
        beforeSend : function(){
            console.log('deleting product');
        },
        success : function(response){
            $('#wishlist-list').html(response.data)
            window.location.reload()
        }
    })
})

})

