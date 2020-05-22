
        	var propselected = null;
        	var wordselected = null;
			var reslen = null;

			function cleanup()
			{
				$("#o1,#o2,#o3").removeClass().addClass("orderunchecked");
			}

            function loadstuff(a,obj)
            {
            	if(propselected == null)
		{
			propselected=obj;
			obj.style.borderTop='2px solid #6ca';
			obj.style.borderLeft='2px solid #6ca';
			obj.style.borderRight='2px solid #6ca';
			obj.style.borderBottom='2px solid #6ca';
			obj.style.color='white';
			obj.style.backgroundColor='#6ca';
			//obj.style.border='2px solid #0fc';
		}else
		{
			propselected.style.border='none';
			propselected.style.backgroundColor='white';
			propselected.style.color='black';
			propselected=obj;
			obj.style.borderTop='2px solid #6ca';
			obj.style.borderLeft='2px solid #6ca';
			obj.style.borderRight='2px solid #6ca';
			obj.style.borderBottom='2px solid #6ca';
			obj.style.color='white';
			obj.style.backgroundColor='#6ca';
			//obj.style.border='2px solid #0fc';
		}

            	//$('#results').show();
            	$("#ResultsHeader").html("");
		$("#ResultsHeader").css({"display":"none"});
            	$("#filteredads").empty();

            	$.ajax({ url:a,
            			 success: function(html)
            			{
            				$("#results").html(html);
            				reslen = $('#results a').length;
            				initPagination();
            				//.animate({ backgroundColor: "#ccff99" }, 500);
            				//$('#results a').css({'color' : '#fc3'});
            				var opt = a.split('=')[1];
            				switch(opt){
            					case "0":
            					    cleanup();$("#o1").removeClass().addClass('orderchecked');
            					    break;
            					case "1":
            					    cleanup();$("#o2").removeClass().addClass('orderchecked');
            					    break;
            					case "2":
            					    cleanup();$("#o3").removeClass().addClass('orderchecked');
            					    break;
            					default:
            					    cleanup();
            				}
            			}
            		   })
            }
            function ShowTopBar()
            {
            	$("#ResultsHeader").html("");
				$("#ResultsHeader").css({"display":"none"});
            	$("#filteredads").empty();
            	//need to include jq-ui for anim to work $("#TopBar").show("slide", { direction: "up" }, 1000);
            	$("#TopBar").show();

            }


	function loadads(a, obj)
	{
		if(wordselected == null)
		{
			wordselected=obj;
			obj.style.border='2px solid #6ca';
			obj.style.color='white';
			obj.style.backgroundColor='#6ca';
			//obj.style.border='2px solid #0fc';

		}else
		{
			wordselected.style.border='2px solid white';
			wordselected.style.color='black';
			wordselected.style.backgroundColor='white';
			wordselected=obj;
			obj.style.border='2px solid #6ca';
			obj.style.color='white';
			obj.style.backgroundColor='#6ca';
			//obj.style.border='2px solid #0fc';
		}

		$.ajax({ url:a,
				 success: function(html)
				{
					$("#TopBar").hide();

					//$("#topprops").hide("slide", { direction: "up" }, 1000);
					//$("#Pagination").hide("slide", { direction: "up" }, 200);
					//$("#Searchresult").hide("slide", { direction: "up" },1000);
					$("#filteredads").html(html).show("slide", { direction: "down" }, 1000);
					var v = $(wordselected).text();
					var p = $(propselected).text();
					$("#ResultsHeader").html("<span class='resultheader' style='color:#298;'>Results - </span><span class='resultheader'>"+p+" -</span>&nbsp;&nbsp;<span class='resultheader'>"+v+"</span>&nbsp;<button id='UnfilterButton' style='display:none;' onclick='$(\".ftext\").remove();$(\".adlist\").each(function(){$(this).show()});$(this).css({\"display\":\"none\"});'>Show All</button> <img id='ShowTB' style='width:22px;height:22px;position:relative;top:5px;' alt='Go Back' title='Go Back' src='/stylesheets/reup.png' onclick='ShowTopBar();'>");
					$("#ResultsHeader").css({"display":"block","backgroundColor":"#f9f8f7"});

				},
				error: function (XMLHttpRequest, textStatus, errorThrown)
				{
					alert(errorThrown);
				}

			   })
	}
	function markup(a)
	{
		b='.'+a;
		$(b).animate({ backgroundColor: "#bbb" }, 500);
	}
var colors = ['dee5b9', 'e0ecdf', 'dfe2ff', 'e0d5f9', 'a1d7eb', 'ff99aa', 'ffcc99', 'ebaca1', 'faccb3', 'f3d793', 'ffffc8', 'b9ffaf', 'acf', 'fea', 'd4e9fc', 'aaffdd'];
     function filterThis(obj) {
	$("#UnfilterButton").css({"display":"inline"});
		    var filtertext = $(obj).text();
		    $("#ResultsHeader").append("<span style='background-color:#"+colors[Math.floor(15*Math.random())]+";' class=ftext>filter:"+filtertext+"<span>");
		    //alert($('.adlist:contains('+filtertext+')').length);
		    $('.adlist').each(function()
			{
				if ( ($(this).textContent || $(this).innerText || $(this).text() || '').toLowerCase().indexOf(filtertext.toLowerCase()) < 0)
				{
					$(this).hide();

				}
			});

		 }
function sortasc(prop)
{
	$(".col1 div").sort(
		function (a,b)
		{ 
		 if($(a).children("."+prop).text() > $( b).children("."+prop).text())
		    return -1;
		 else
		    return 1;
		}
        ).appendTo(".col1");
        $("#tog"+prop+"dn").css({"display":"inline"});$("#tog"+prop+"up").css({"display":"none"});
}
function sortdes(prop)
{
	$(".col1 div").sort(
		function (a,b)
		{ 
		 if($(a).children("."+prop).text() > $( b).children("."+prop).text())
		    return 1;
		 else
		    return -1;
		}
        ).appendTo(".col1");
        $("#tog"+prop+"up").css({"display":"inline"});$("#tog"+prop+"dn").css({"display":"none"});
}
function addToggle(subp, idx)
{
	$("#tog"+subp).toggle(function (eventobj)
		{
			var subp = eventobj.target.id.slice(3);
			// move selected prop to begining of the row
			$("."+subp).each(function(index){$(this).parent().prepend(this);});
			// add bg border colors to row and right side prop
			$("."+subp).css({ "background-color": "#"+colors[15-idx] });
			$(this).css({"border-left":"1px solid #777","border-top":"1px solid #777","background-color":"#"+colors[15-idx]});
			//add sort bottons and sort desc
			$("#tog"+subp+"dn").css({"display":"inline"});
			$("#tog"+subp+"up").css({"display":"none"});
			$(".col1 div").sort(
					  function (a,b)
					  {
					   if($(a).children("."+subp).text() > $(b).children("."+subp).text())
						  return -1;
					   else
						  return 1;
					  }
			).appendTo(".col1");
			$(".col2").data("on").push(subp);
		}
		,function (eventobj)
		{
			var subp =eventobj.target.id.slice(3);
			$(".adlist span[class!="+subp+"]").css({"display":"inline"});
			$("."+subp).css({ "background-color": "#fff" });
			$(this).css({"background-color":"#fff","border":"0px none"});
			$("#tog"+subp+"dn").css({"display":"none"});
			$("#tog"+subp+"up").css({"display":"none"});
			var rem= $(".col2").data("on").indexOf(subp);
			$(".col2").data("on").splice(rem,1);
		});
}
function getPropUrl()
{
	s = $(propselected)[0].attributes['onclick'].value;
	return s.substring(s.indexOf('/'),s.indexOf('?'));
}
function onlyHighlights(obj)
{
	var ons=$('.col2').data("on")
	$(".adlist span").toggle();
	for(var i=0;i<ons.length;i++){
		$(".adlist span[class="+ons[i]+"]").toggle();
	}
	var butt = $(obj.target);
	if(butt.text() == "Off"){
		butt.text('On');
		butt.removeClass().addClass('toff');
	}else{
		butt.text('Off');
		butt.removeClass().addClass('ton');
	}
	
}

function initScrolling()
{
	$(window).scroll(function(){
		var offset=$(document).scrollTop();
		if (offset > 85)
			offset = offset - 85 +'px';
		else
			offset = '0px';
		$(".col2").animate({paddingTop:offset},{duration:300,queue:false});
	});
	$(".adlist span").hover(
			function () {
				//$(this).css("text-decoration", "underline");
				$(this).css("border-bottom", "1px solid red");
			},
			function () {
				//$(this).css("text-decoration", "none");
				$(this).css("border-bottom", "none");
			}
	);
}