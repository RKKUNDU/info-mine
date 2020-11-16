$(document).ready(function(){
    var frm = $('form');
    $("form").submit(function (e) {

        e.preventDefault();
        // var formData = JSON.parse(JSON.stringify(jQuery('form').serializeArray()));
        var myObject = new Object();
        myObject.name = $("#name").val();
        myObject.mobile_no = $("#whatsappnumber").val();
        myObject.ldap_email = $("#ldapusername").val();
        myObject.ldap_password = $("#ldappassword").val();
        myObject.cse_email = $("#deptmailusername").val();
        myObject.cse_email_pass = $("#deptmailpassword").val();
        myObject.moodle_id = $("#moodleusername").val();
        myObject.moodle_pass = $("#moodlepassword").val();
        var formData = JSON.stringify(myObject);
        console.log(formData);
        $.ajax({
            type: frm.attr('method'),
            url: frm.attr('action'),
            dataType : 'json',
            data: formData,
            success: function (data) {
                alert('Submission was successful.');
                console.log(data);
            },
            error: function (data) {
                console.log('An error occurred.');
                console.log(data);
            },
        });
    });
  });