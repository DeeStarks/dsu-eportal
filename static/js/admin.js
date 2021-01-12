$(function(){
    // sidebar display
    $(".navbar .nav_items .fa-bars").click(function(){
        $(".sidebar").css({"right": "0"})
    })
    $(".sidebar .side_in .side_profile i").click(function(){
        $(".sidebar").css({"right": "-100%"})
    })

    // Dashboard sidebar
    $(".side_nav .side_in .side_profile i").click(function(){
        $(".side_nav").css({"left": "-300px"})
        $(".main_body").css({"padding": "100px 50px 50px 90px"})
        $(".contact_bg h3").css({"margin-left": "150px"})
    })
    $(".open_side").click(function(){
        $(".side_nav").css({"left": "0"})
        $(".main_body").css({"padding": "100px 50px 50px 350px"})
        $(".contact_bg h3").css({"margin-left": "350px"})
    })

    // Thumbnail name display
    $('#accordion #thumbnail').change(function() {
        var i = $(this).prev('label').clone();
        var file = $('#accordion #thumbnail')[0].files[0].name;
        $("#thumbnail_name").html(file)
        $(this).prev('label').text(file);

        readURL(this);
    });

    function readURL(input) {
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            
            reader.onload = function(e) {
            $('#thumbnail_preview').attr('src', e.target.result);
            }
            
            reader.readAsDataURL(input.files[0]);
        }
    }

    $(document).ready(function() {
        $("#sort").DataTable({
            columnDefs : [
                { type : 'date', targets : [3] }
            ],  
        });
    });

})

// Admin Panel Dashboard Chart
let admin01 = document.getElementById("adminChart01").getContext('2d');
let admin02 = document.getElementById("adminChart02").getContext('2d');

let adminChart01 = new Chart(admin01, {
    type: 'bar',
    data: {
        labels: ['100L', "200L", "300L", "400L"],
        datasets: [{
            label: 'Percentage',
            data: [40.02, 10.0, 30.2, 0],
            backgroundColor: '#00205a',
            fill: false,
            borderColor: '#00205a',
            borderWidth: 1,
        }]
    },
    options: {
        title: {
            display: true,
            text: 'Students Total Performance'
        }
    }
})

let adminChart02 = new Chart(admin02, {
    type: 'doughnut',
    data: {
        labels: ["100L", "200L", "300L", "400L"],
        datasets: [{
            label: 'Percentage',
            data: [49.89, 12.47, 37.65, 0],
            backgroundColor: [
                "#00205a",
                '#00ff1e',
                '#ff6347',
                "#ff7b00"
            ],
            fill: false,
            borderColor: 'transparent',
            borderWidth: 2,
            weight: 2
        }]
    },
    options: {
        title: {
            display: true,
            text: 'Students Performance by Percentage'
        }
    }
})
