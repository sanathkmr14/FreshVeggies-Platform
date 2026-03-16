// ===== FreshVeggies — Main JavaScript =====

$(document).ready(function () {

    // Helper to get CSRF token
    function getCSRFToken() {
        return document.querySelector('meta[name="csrf-token"]').getAttribute('content');
    }

    // ===== Plus Cart =====
    $('.plus-cart').click(function () {
        var id = $(this).attr("pid").toString();
        var qtyEl = document.getElementById("qty-" + id);

        $.ajax({
            type: "POST",
            url: "/pluscart/",
            data: { 
                prod_id: id,
                csrfmiddlewaretoken: getCSRFToken()
            },
            success: function (data) {
                if (qtyEl) qtyEl.innerText = data.quantity;
                document.getElementById("amount").innerText = data.amount;
                document.getElementById("totalamount").innerText = data.totalamount;
            }
        });
    });

    // ===== Minus Cart =====
    $('.minus-cart').click(function () {
        var id = $(this).attr("pid").toString();
        var qtyEl = document.getElementById("qty-" + id);

        $.ajax({
            type: "POST",
            url: "/minuscart/",
            data: { 
                prod_id: id,
                csrfmiddlewaretoken: getCSRFToken()
            },
            success: function (data) {
                if (qtyEl) qtyEl.innerText = data.quantity;
                document.getElementById("amount").innerText = data.amount;
                document.getElementById("totalamount").innerText = data.totalamount;
            }
        });
    });

    // ===== Remove Cart =====
    $('.remove-cart').click(function () {
        var id = $(this).attr("pid").toString();
        var cartItem = document.getElementById("cart-item-" + id);

        $.ajax({
            type: "POST",
            url: "/removecart/",
            data: { 
                prod_id: id,
                csrfmiddlewaretoken: getCSRFToken()
            },
            success: function (data) {
                if (cartItem) {
                    cartItem.style.transition = "all 0.3s ease";
                    cartItem.style.opacity = "0";
                    cartItem.style.transform = "translateX(-20px)";
                    setTimeout(function () { 
                        cartItem.remove(); 
                        
                        // Check if cart is empty
                        var remainingItems = document.querySelectorAll('.cart-item').length;
                        if (remainingItems === 0) {
                            window.location.reload();
                        }
                    }, 300);
                }
                
                document.getElementById("amount").innerText = data.amount;
                document.getElementById("totalamount").innerText = data.totalamount;
                
                var cartCount = document.querySelector('.cart-count');
                if (cartCount && data.cart_count !== undefined) {
                    cartCount.innerText = data.cart_count;
                }
            }
        });
    });

});