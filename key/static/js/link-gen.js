

$(uuidinput).change(function(){
 console.log("hello world")
 var input = $(this).val();
 var oldUrl = $("#bbb").attr("href");
 var newUrl = oldUrl.replace("uuid", input);
 $("#bbb").attr("href", newUrl);
});
