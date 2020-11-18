$(document).ready(function(){
    var frm = $('form');
    $("form").submit(function (e) {

        e.preventDefault();
        var formData = JSON.parse(JSON.stringify(jQuery('form').serializeArray()))
        $.ajax({
            type: frm.attr('method'),
            url: frm.attr('action'),
            dataType : 'json',
            data: formData,
            success: function (data) {
                console.log('Submission was successful.');
                console.log(data);
            },
            error: function (data) {
                console.log('An error occurred.');
                console.log(data);
            },
        });
    });
  });