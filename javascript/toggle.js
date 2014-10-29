/*
  This is a simple javascript library which
  will toggle the visibility of a div element
  in an html document and scroll to the #middle_cgi
  div element on the page.

  Dependency: jQuery
*/

//accepts the id of the element that called the function
function toggle_visibility(button_id)
{
    //get a reference to the relevant div containers
    var background = document.getElementById("background_on");
    var motivation = document.getElementById("motivation_on");

    //show / hide the appropriate container
    if(button_id == "bg")
    {
	background.className="show";
	motivation.className="hide";
    }
    else if (button_id == "mtv")
    {
	motivation.className="show";
	background.className="hide";
    }

}

//jquery function to scroll to the #middle_cgi div
//if we click one of the navigation buttons at the top
$( document ).ready(function() {
    
    //regex to determine if the link we clicked was for page 1
    var pageOne = /page=1$/;
    var page = /page/;
    
    //Only scroll to the first page of the story
    if(document.location.href.match(pageOne))
    {
	//$("html, body").animate({ scrollTop: $("#middle_cgi").offset().top }, 1000);
    }
    
    else if (document.location.href.match(page))
    {
	//if it is a regular page, don't scroll at all
	//$("html, body").scrollTop($("#middle_cgi").offset().top);
    }    
    else
    {
	//scroll for the stats page and the home page
	$("html, body").animate({ scrollTop: $("#middle_cgi").offset().top }, 1000);
    }
});
