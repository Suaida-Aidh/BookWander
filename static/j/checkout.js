$(document).ready(function () {
    $('.payWithRazorpay').click(function (e) {
        e.preventDefault();
        console.log('___________________________________________')


        var first_name = $("[name='first_name']").val();
        
        var billing_address = $("[name='billing_address']").val();

        var last_name = $("[name='last_name']").val();
        var email = $("[name='email']").val();
        var phone = $("[name='phone']").val();
        var address = $("[name='address']").val();
        var city = $("[name='city']").val();
        var state = $("[name='state']").val();
        var country = $("[name='country']").val();
        var pincode = $("[name='pincode']").val();
        var token = $("[name='csrfmiddlewaretoken']").val();

        console.log(first_name, last_name, email, phone, address,city,state,country, pincode);
        // if (first_name == "" || last_name == "" || email == "" || phone == "" || address == "" || city == "" || state == "" || country == "" || pincode == "") {

        //     swal({
        //         title: "warning!",
        //         text: "All fields are mandatory!",
        //         icon: "warning",
        //         button: "Ok",
        //     });
        //     return false;
        // }
        // else {
            $.ajax({
                method: "GET",
                url: "/order/proceed-to-pay/",
                success: function (response) {
                    console.log(response);
                    var options = {
                        "key": "rzp_test_0Wy5u2AUufd1LA", // Enter the Key ID generated from the Dashboard
                        "amount": response.total_price *100,//response.total_price *100 , // Amount is in currency subunits. Default currency is INR. Hence, 50000 refers to 50000 paise
                        "currency": "INR",
                        "name": "Bookwander",
                        "description": "Thank you",
                        "image": "https://example.com/your_logo",
                        // "order_id": "order_IluGWxBm9U8zJ8", //This is a sample Order ID. Pass the `id` obtained in the response of Step 1
                        "handler": function (responseb) {
                            // alert(responseb.razorpay_payment_id);
                            // alert(response.razorpay_order_id);
                            // alert(response.razorpay_signature)
                            data = {
                                // "first_name": first_name,
                                // "last_name": last_name,
                                // "email": email,
                                // "phone": phone,
                                // "address": address,
                                // "city": city,
                                // "state": state,
                                // "country": country,
                                // "pincode": pincode,
                                "billing_address": billing_address,
                                "payment_mode": "Paid by Razorpay",
                                "payment_id": responseb.razorpay_payment_id,
                                csrfmiddlewaretoken: token

                            }
                            $.ajax({
                                
                                method: "POST",
                                url: "/order/place_order/new/",
                                data: data,
                                success: function (responsec) {

                                    swal(
                                        "Congratulations!", responsec.status, "success"
                                    ).then(value => {
                                        window.location.href = '/order/my-orders/'
                                    })

                                },
                              
                            });
                        },
                        "prefill": {
                            "name": first_name + " " + last_name,
                            "email": email,
                            "contact": phone
                        },
                        "notes": {
                            "address": "bookwander shopping site"
                        },
                        "theme": {
                            "color": "#3399cc"
                        }
                    };
                    var rzp1 = new Razorpay(options);
                    rzp1.open();


                }
            });

        // }




    });
});