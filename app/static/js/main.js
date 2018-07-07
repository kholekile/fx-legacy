$(function() {
    $('#church_details').hide(); 
    $('#friend_details').hide(); 

    $('#inputReferredByOption').change(function(){
        if($('#inputReferredByOption').val() == 'church_pastor') {
            $('#church_details').toggle("slow");
            $('#friend_details').hide();
            document.getElementById('inputReferrerTitle').removeAttribute("required");
            document.getElementById('inputReferrerFirstName').removeAttribute("required");
            document.getElementById('inputReferrerLastName').removeAttribute("required");
            document.getElementById('inputReferrerContact').removeAttribute("required"); 
        } 
        else if ($('#inputReferredByOption').val() == 'friend') {
            $('#friend_details').toggle("slow"); 
            $('#church_details').hide();
            document.getElementById('inputChurchOrganisation').removeAttribute("required");
        } 
        else if ($('#inputReferredByOption').val() == 'no_one') {
            $('#friend_details').hide(); 
            $('#church_details').hide();
            document.getElementById('inputChurchOrganisation').removeAttribute("required");
            document.getElementById('inputReferrerTitle').removeAttribute("required");
            document.getElementById('inputReferrerFirstName').removeAttribute("required");
            document.getElementById('inputReferrerLastName').removeAttribute("required");
            document.getElementById('inputReferrerContact').removeAttribute("required"); 
        }
    });

});

$(function() {
    $('#form-section').hide(); 
});

function unhideForm(){
     $('#form-section').toggle("slow");
}

function isNumberKey(evt){
    var charCode = (evt.which) ? evt.which : evt.keyCode
    return !(charCode > 31 && (charCode < 48 || charCode > 57));
}