$(document).ready(function(){
    
    
    
    $("#badgeManagerForm select[name=name]").change(function(){
        var value = $(this).val();
        if (!value == '' || !value =='none') {
            $("#userBadges").fadeIn(600);
            if (!$("#badgeManagerForm select[name=badge]").val()=='' || !$("#badgeManagerForm select[name=badge]").val() =='none') {
                $(".addRemoveBadges").removeClass('disabled');
            }
        }else{
            $('#userBadges').fadeOut(600);
            $(".addRemoveBadges").addClass('disabled');
        }
    });
    
    
    
    $("#badgeManagerForm select[name=badge]").change(function(){
        var value = $(this).val();
        if ((!value == '' || !value =='none') && $("#userBadges").is(':visible')) {
            $(".addRemoveBadges").removeClass('disabled');
        }else{
            $(".addRemoveBadges").addClass('disabled');
        }
    });
    
    
    
    $("#editBadgeForm select[name=badge]").change(function(){
        var value = $(this).val();
        if (!value == '' || !value =='none') {
            //code
            $.ajax({
                url: badgeInfoURL,
                method: "POST",
                data: { badgeID : value },
                dataType: "json"
            }).done(function(response){
                console.log(response.badgeLink);
                $("#editBadgeForm input[name=name]").val(response.badgeName);
                $("#editBadgeForm input[name=link]").val(response.badgeLink);
                $("#editBadgeForm input[name=imageurl]").val(response.badgeImageURL);
            });
        }
    });
    
    
    
    
    $("#createBadgeForm").ajaxForm({ 
        success:        function(responseText){
            console.log(responseText);
            if (responseText.success) {
                //code
                alert("Success");
                location.reload();
            }else{
                alert(responseText.error);
            }
        },
        dataType:       'json',
        timeout:        3000,
    });
    
    
    
    $("#editBadgeForm").ajaxForm({ 
        success:        function(responseText){
            console.log(responseText);
            if (responseText.success) {
                //code
                alert("Success");
                location.reload();
            }else{
                alert(responseText.error);
            }
        },
        dataType:       'json',
        timeout:        3000,
    });
    
    
    
    $("#badgeManagerForm").ajaxForm({ 
        success:        function(responseText){
            console.log(responseText);
            if (responseText.success) {
                //code
                alert("Success");
                location.reload();
            }else{
                alert(responseText.error);
            }
        },
        dataType:       'json',
        timeout:        3000,
    });
    
    
    
    $("#userBadges").click(function(){
        var value = $("#badgeManagerForm select[name=name]").val();
        $.ajax({
                url: badgeDisplayURL,
                method: "POST",
                data: { userInfoID : value },
                dataType: "html"
            }).done(function(response){
                console.log(response);
                $("#displayBadges .modal-content").html(response);
                $("#displayBadges").modal("show");
            });
        
    });
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
});