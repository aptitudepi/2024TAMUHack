var scrollTop =  window.pageYOffset || document.documentElement.scrollTop;
var scrollLeft = window.pageXOffset || document.documentElement.scrollLeft;
var iMap = document.getElementById("iMap");
var imgC = document.getElementById("imgC");
var map1Active = true;
var smallSide;
var cont=false;
var scaleAmt = 1.0;
var originalX = 0;
var originalY = 0;
var diffX = 0;
var diffY = 0;
var viewWidth = window.innerWidth;
var viewHeight = window.innerHeight;
var paddingI = parseInt($(".roomToggle").css("padding"));
var fontSizeI = parseInt($(".roomToggle").css("font-size"));
var roomToggles = document.getElementsByClassName(".roomToggle");
var roomTogglesWidth = [];
var cPadding; 
var cFontSize;
var scrollToggleActive = false;
//these are flags that show which side to stop (or none if 0)
var stopLeft = 0;
var stopRight = 0;
var stopTop = 0;
var stopBottom = 0;
//these variables are the number of rooms that have a room 
//number with the prefix 'a', 'b', etc.
var aRoomNum = 23;
var bRoomNum = 0;
var dataArr;
var roomListArr;
//these variables are used to indicate if the icon popup width should be set or not
var icon1SetW = true;
var icon2SetW = true;
var icon3SetW = true;
var stopHoverTrig1 = false;
var stopHoverTrig2 = false;
var stopHoverTrig3 = false;

function sleep(milliseconds) {
  const date = Date.now();
  let currentDate = null;
  do {
    currentDate = Date.now();
  } while (currentDate - date < milliseconds);
} 
function stopDefault(e) {
  e.preventDefault();
}
var wheelEvent = 'onwheel' in document.createElement('div') ? 'wheel' : 'mousewheel';
function disableScroll() {
  window.addEventListener('DOMMouseScroll', stopDefault, {passive: false});
  window.addEventListener(wheelEvent, stopDefault, {passive: false});
  window.addEventListener('touchmove', stopDefault, {passive: false});
}
function enableScroll() {
  window.removeEventListener('DOMMouseScroll', stopDefault, {passive: false});
  window.removeEventListener(wheelEvent, stopDefault, {passive: false}); 
  window.removeEventListener('touchmove', stopDefault, {passive: false});
}
function fixToggleWidth() {
  for (var index10 = 0; index10 < roomToggles.length; index10++) {
    //roomToggles[index10].style.width = roomTogglesWidth[index10];
    roomToggles[index10].style.maxWidth = "auto !important";
  }
}

fetch('/static/map.json').then(function(resp) {
  return resp.json();
  }).then(function(data) {
  dataArr = data.mainInfo; //this can now be indexed using [index] notation
  roomListArr = data.roomInfo2;
  try { updateClubListing(); }
  catch(err) {}//do nothing
  });
$(document).ready(function() {
  for (var index10 = 0; index10 < roomToggles.length; index10++) {
    roomTogglesWidth.push(roomToggles[index10].offsetWidth);
  }
$("#A001").css("left", `${5}%`);
$("#A001").css("top", `${54}%`);
$("#A002").css("left", `${10}%`);
$("#A002").css("top", `${47.5}%`);
$("#A003").css("left", `${15.25}%`);
$("#A003").css("top", `${39}%`);
$("#A006").css("left", `${36}%`);$("#A006").css("top", `${26}%`);$("#A009").css("left", `${55.25}%`);$("#A009").css("top", `${26}%`);$("#A013").css("left", `${81.5}%`);$("#A013").css("top", `${48}%`);$("#A015").css("left", `${22}%`);$("#A015").css("top", `${56}%`);$("#A016").css("left", `${32}%`);$("#A016").css("top", `${48}%`);$("#A017").css("left", `${37.6}%`);$("#A017").css("top", `${44.5}%`);$("#A018").css("left", `${52.5}%`);$("#A018").css("top", `${42}%`);$("#A019").css("left", `${60}%`);$("#A019").css("top", `${48}%`);$("#A021").css("left", `${73}%`);$("#A021").css("top", `${58}%`);$("#A023").css("left", `${87}%`);$("#A023").css("top", `${72}%`);
$("#B001").css("left", `${6.5}%`);$("#B001").css("top", `${54.5}%`);$("#B003").css("left", `${17}%`);$("#B003").css("top", `${41.5}%`);$("#B005").css("left", `${36.5}%`);$("#B005").css("top", `${27.5}%`);$("#B007").css("left", `${54}%`);$("#B007").css("top", `${27.5}%`);$("#B010").css("left", `${74.5}%`);$("#B010").css("top", `${43}%`);$("#B015").css("left", `${71.5}%`);$("#B015").css("top", `${57}%`);$("#B018").css("left", `${87}%`);$("#B018").css("top", `${73}%`);
  //this is necessary right before the organization image centering so that it always executes correctly
  sleep(20);
});

$("img").on('dragstart', function(event) {event.preventDefault();});
$('img').bind('contextmenu', function(e) {return false;}); 
$("#icon1").on('click', function() {
    stopHoverTrig1 = true;
});
$("#icon2").on('click', function() {
    stopHoverTrig2 = true;
});
$("#icon3").on('click', function() {
    stopHoverTrig3 = true;
});
$(".nav1").on('click', function() {
	iMap.src="/static/STEAM-map-01.svg";
  $(".floorNum").text("1");
  //this is just used to clear the past class changes
  $(".nav1C").removeClass("active");
  $(".nav2C").removeClass("active");
  $(".nav1C").addClass("active");
  //this contains all of the 'a' rooms
  $(".imgC7").css("display", "block");
  //this contains all of the 'b' rooms
  $(".imgC8").css("display", "none");
  map1Active = true;
});
$(".nav2").on('click', function() {
	iMap.src="/static/STEAM-map-02.svg";
  $(".floorNum").text("2");
    //this is just used to clear the past class changes
    $(".nav1C").removeClass("active");
    $(".nav2C").removeClass("active");
    $(".nav2C").addClass("active");
    $(".imgC7").css("display", "none");
    $(".imgC8").css("display", "block");
  map1Active = false;
});
$(".nav3").on('click', function() {
    if (!scrollToggleActive) { //turn on disable scrolling
      $(".nav3C").addClass("active");
      $(".scrollToggle").text("on");
      //scrollToggle
      disableScroll();
    }
    else { //turn off disable scrolling
      $(".nav3C").removeClass("active");
      $(".scrollToggle").text("off");
      enableScroll();
    }
    scrollToggleActive = !scrollToggleActive;
});
$(".imgC6").on('click', function() { //open more info bar
  $(".imgC6").css("display","none");
  $(".legendC").css("display","block");
  $(".legendC").css("z-index","99");
  $(".roomToggle").css("z-index","1");
});
$(".closeInfo").on('click', function() { //close more info bar
  $(".legendC").css("display","none");
  $(".imgC6").css("display","block");
});
$(".imgC6Mobile").on('click', function() { //open more info bar
  $(".imgC6Mobile").css("display","none");
  $(".legendCMobile").css("display","block");
  $(".legendCMobile").css("z-index","99");
  $(".roomToggle").css("z-index","1");
});
$(".closeInfoMobile").on('click', function() { //close more info bar
  $(".legendCMobile").css("display","none");
  $(".imgC6Mobile").css("display","block");
});
function mouseMoveCode(event) {
  try {
    var currentX;
    var currentY;
    if (viewWidth < 821) { //if they are currently on mobile, get these coordinates
      currentX = event.originalEvent.touches[0].pageX;
      currentY = event.originalEvent.touches[0].pageY;
    }
    else {
      currentX = event.pageX;
      currentY = event.pageY;
    }
    if (scaleAmt == 1.0) {
    	diffX = 0;
      diffY = 0;
      $(".roomToggle").css("z-index","1");
      for (var index3 = 0; index3 < dataArr.length; index3++) {
        $(`#${dataArr[index3].room}`).css("left", `${dataArr[index3].left}%`);
        $(`#${dataArr[index3].room}`).css("top", `${dataArr[index3].top}%`);
      }
    }
    else {
      $(".roomToggle").css("z-index","1");
      var tempW;
      var tempH;
      for (var index3 = 0; index3 < dataArr.length; index3++) {
       tempW = viewWidth/118 - (viewWidth/10000);
       tempH = 4;
      if (viewWidth > 1900) {
        tempW -= 3.0;
        tempH = 7;
      }
      else if (viewWidth > 1800) {
        tempW -= 2.5;
        tempH = 7;
      }
      else if (viewWidth > 1700) {
        tempW -= 1.5;
        tempH = 7;
      }
      else if (viewWidth > 1600) {
        tempW -= 0.5;
        tempH = 7;
      }
      else if (viewWidth > 1500) {
        tempH = 7;
      }
      else if (viewWidth > 1050) {
        tempH = 6;
       }
       else if (viewWidth > 950) {
        tempH = 5;
       }
       else if (viewWidth > 850) {
        tempH = 4;
       }
       else if (viewWidth > 650) {
        tempH = 3.5;
       }
       else if (viewWidth > 550) {
        tempH = 3;
       }
       else if (viewWidth > 450) {
        tempH = 2.5;
       }
       else if (viewWidth > 0) {
        tempH = 2;
       }
        $(`#${dataArr[index3].room}`).css("left", `${(dataArr[index3].left)*scaleAmt+(iMap.getBoundingClientRect().left - imgC.getBoundingClientRect().left)/(tempW)+scaleAmt}%`);
        $(`#${dataArr[index3].room}`).css("top", `${(dataArr[index3].top)*scaleAmt+(iMap.getBoundingClientRect().top - imgC.getBoundingClientRect().top)/(tempH)}%`);
      }
    }
    iMap.style.marginLeft = `${diffX}px`;
    iMap.style.marginTop = `${diffY}px`;
    if (cont && scaleAmt!=1.0) {
    //stop the map from trying to move left
    if (stopLeft == 1 && (-(originalX - currentX)/-1)<0) {}
    //stop the map from trying to move right
    else if (stopRight == 1 && (-(originalX - currentX)/-1)>0) {}
    else {diffX += -(originalX - currentX);}
    //stop the map from trying to move up
    if (stopTop == 1 && (-(originalY - currentY)/-1)<0) {}
    //stop the map from trying to move down
    else if (stopBottom == 1 && (-(originalY - currentY)/-1)>0) {}
    else {diffY += -(originalY - currentY);}
    iMap.style.marginLeft = `${diffX}px`;
    iMap.style.marginTop = `${diffY}px`;
    if ((iMap.getBoundingClientRect().left - imgC.getBoundingClientRect().left) > 0) {
        //set the trigger to make it stop moving left
        stopLeft = 1; //stop moving left
    }
    else {
      stopLeft = 0;
    }
    if ((iMap.getBoundingClientRect().right - imgC.getBoundingClientRect().right) < 0) {
        //set the trigger to make it stop moving right
        stopRight = 1; //stop moving right
    }
    else {
      stopRight = 0;
    }
    if ((iMap.getBoundingClientRect().top - imgC.getBoundingClientRect().top) > 0) {
        //set the trigger to make it stop moving up
        stopTop = 1; //stop moving up
    }
    else {
      stopTop = 0; 
    }
    if ((iMap.getBoundingClientRect().bottom - imgC.getBoundingClientRect().bottom) < 0) {
        //set the trigger to make it stop moving down
        stopBottom = 1; //stop moving down
    }
    else {
      stopBottom = 0;
    }
  }
    originalX = currentX;
    originalY = currentY;
}
catch (err) {
  //if the user hovers over the map before dataArr gets its data from 
  //map.json, then an error will be thrown- this gets rid of the error
  console.log("Don't hover over the map so soon!");
}
}
$(".imgC").on("touchstart mousedown", function(e) {
  imgC.style.height = `${imgC.offsetHeight}px`;
  cont = true;
  if (viewWidth < 821) { //if they are currently on mobile, get these coordinates
    originalX = e.originalEvent.touches[0].pageX;
    originalY = e.originalEvent.touches[0].pageY;
  }
  else {
    originalX = e.pageX;
    originalY = e.pageY;
  }
});
$("body").on("touchend mouseup", function(){
  cont = false;
});
$(".imgC").on("touchmove mousemove", function(event){
  mouseMoveCode(event);
});
$(".imgC3").on('click', function(event) { //zoom in
  fixToggleWidth();
  $(".imgC9").css("display","none");
  scaleAmt+=1.0;
  if (scaleAmt > 5.0) {
    scaleAmt = 5.0;
  }
  if (scaleAmt != 1.0){
    cPadding = ((scaleAmt + paddingI)>8)? 8: scaleAmt + paddingI;
    cFontSize = ((scaleAmt*2 + fontSizeI)>20)? 20: scaleAmt*2 + fontSizeI;
    $(".roomToggle").css("padding", `${cPadding}px`);
    $(".roomToggle").css("font-size", `${cFontSize}px`);
    $(".roomToggle").css("z-index","1");
    $(".roomToggle").css("max-width","100%");
    //$("#A015").css("width","auto");
    $("#A023").css("max-width","100% !important");
    $("#B018").css("max-width","100% !important");
    var tempW;
      var tempH;
      for (var index3 = 0; index3 < dataArr.length; index3++) {
       tempW = viewWidth/118 - (viewWidth/10000);
       tempH = 4;
      if (viewWidth > 1900) {
        tempW -= 3.0;
        tempH = 7;
      }
      else if (viewWidth > 1800) {
        tempW -= 2.5;
        tempH = 7;
      }
      else if (viewWidth > 1700) {
        tempW -= 1.5;
        tempH = 7;
      }
      else if (viewWidth > 1600) {
        tempW -= 0.5;
        tempH = 7;
      }
      else if (viewWidth > 1500) {
        tempH = 7;
      }
      else if (viewWidth > 1050) {
        tempH = 6;
       }
       else if (viewWidth > 950) {
        tempH = 5;
       }
       else if (viewWidth > 850) {
        tempH = 4;
       }
       else if (viewWidth > 650) {
        tempH = 3.5;
       }
       else if (viewWidth > 550) {
        tempH = 3;
       }
       else if (viewWidth > 450) {
        tempH = 2.5;
       }
       else if (viewWidth > 0) {
        tempH = 2;
       }
        $(`#${dataArr[index3].room}`).css("left", `${(dataArr[index3].left)*scaleAmt+(iMap.getBoundingClientRect().left - imgC.getBoundingClientRect().left)/(tempW)+scaleAmt}%`);
        $(`#${dataArr[index3].room}`).css("top", `${(dataArr[index3].top)*scaleAmt+(iMap.getBoundingClientRect().top - imgC.getBoundingClientRect().top)/(tempH)}%`);
      }
  }
  iMap.style.transform = `scale(${scaleAmt})`;
  //$(".imgC2").css("z-index","99");
  $(".imgC3").css("z-index","99");
  $(".imgC4").css("z-index","99");
  $(".imgC6").css("z-index","99");
  $(".imgC6Mobile").css("z-index","99");
  $(".legendC").css("z-index","99");
  $(".legendCMobile").css("z-index","99");
});
$(".imgC4").on('click', function(event) { //zoom out
  fixToggleWidth();
  scaleAmt-=1.0;
  $(".imgC9").css("display","none");
  if (scaleAmt < 1.0) {
    scaleAmt = 1.0;
    $(".imgC9").css("display","block");
  }
  else if (scaleAmt == 1.0) {
    $(".roomToggle").css("max-width","8%");
    $(".imgC9").css("display","block");
  	iMap.style.marginLeft = `${0}px`;
    iMap.style.marginTop = `${0}px`;
    //this resets the roomToggle buttons to their initially-sized styling
    $(".roomToggle").css("padding", `${paddingI}px`);
    $(".roomToggle").css("font-size", `${fontSizeI}px`);
    for (var index3 = 0; index3 < dataArr.length; index3++) {
      $(`#${dataArr[index3].room}`).css("left", `${dataArr[index3].left}%`);
      $(`#${dataArr[index3].room}`).css("top", `${dataArr[index3].top}%`);
    }
    $("#A015").css("max-width","9.25%");

  }
  if (scaleAmt != 1.0) {
    $(".roomToggle").css("max-width","100%");
    $("#A023").css("max-width","100% !important");
    $("#B018").css("max-width","100% !important");
    cPadding = ((scaleAmt + paddingI)>8)? 8: scaleAmt + paddingI;
    cFontSize = ((scaleAmt*2 + fontSizeI)>20)? 20: scaleAmt*2 + fontSizeI;
    $(".roomToggle").css("padding", `${cPadding}px`);
    $(".roomToggle").css("font-size", `${cFontSize}px`);
    $(".roomToggle").css("z-index","1");
    var tempW;
      var tempH;
      for (var index3 = 0; index3 < dataArr.length; index3++) {
       tempW = viewWidth/118 - (viewWidth/10000);
       tempH = 4;
      if (viewWidth > 1900) {
        tempW -= 3.0;
        tempH = 7;
      }
      else if (viewWidth > 1800) {
        tempW -= 2.5;
        tempH = 7;
      }
      else if (viewWidth > 1700) {
        tempW -= 1.5;
        tempH = 7;
      }
      else if (viewWidth > 1600) {
        tempW -= 0.5;
        tempH = 7;
      }
      else if (viewWidth > 1500) {
        tempH = 7;
      }
      else if (viewWidth > 1050) {
        tempH = 6;
       }
       else if (viewWidth > 950) {
        tempH = 5;
       }
       else if (viewWidth > 850) {
        tempH = 4;
       }
       else if (viewWidth > 650) {
        tempH = 3.5;
       }
       else if (viewWidth > 550) {
        tempH = 3;
       }
       else if (viewWidth > 450) {
        tempH = 2.5;
       }
       else if (viewWidth > 0) {
        tempH = 2;
       }
        $(`#${dataArr[index3].room}`).css("left", `${(dataArr[index3].left)*scaleAmt+(iMap.getBoundingClientRect().left - imgC.getBoundingClientRect().left)/(tempW)+scaleAmt}%`);
        $(`#${dataArr[index3].room}`).css("top", `${(dataArr[index3].top)*scaleAmt+(iMap.getBoundingClientRect().top - imgC.getBoundingClientRect().top)/(tempH)}%`);
      }
  }
  iMap.style.transform = `scale(${scaleAmt})`;
  //$(".imgC2").css("z-index","99");
  $(".imgC3").css("z-index","99");
  $(".imgC4").css("z-index","99");
  $(".imgC6").css("z-index","99");
  $(".imgC6Mobile").css("z-index","99");
  $(".legendC").css("z-index","99");
  $(".legendCMobile").css("z-index","99");
});
/*This is for all of the zoom map stuff*/
/*$("#enlarge").click(function(){
  scrollTop =  window.pageYOffset || document.documentElement.scrollTop;
  scrollLeft = window.pageXOffset || document.documentElement.scrollLeft;
  			if (map1Active) {
        	$(".zoomImg").attr("src", "STEAM-map-01.svg");
        }
  			else {
        	$(".zoomImg").attr("src", "STEAM-map-02.svg");
        }
        window.onscroll = function() { 
            window.scrollTo(scrollLeft, scrollTop); //this will disable scrolling
        };
        $(".zoomImgC").css({"display":"block"});
        $(".close").css({"display":"block"});
  			$("body").css({"overflow":"hidden"});
        //$(".imgC2").css("z-index","1");
        $(".imgC3").css("z-index","1");
        $(".imgC4").css("z-index","1");
        $(".imgC6").css("z-index","1");
        $(".imgC6Mobile").css("z-index","1");
        $(".legendC").css("z-index","1");
        $(".legendCMobile").css("z-index","1");
     });*/
     $(".zoomImgC").on('click', function(){
        window.onscroll = function() {}; //enable scrolling
        $(".zoomImgC").css({"display":"none"});
        $(".close").css({"display":"none"});
       $("body").css({"overflow":"auto"});
       $(".legendC").css("z-index","99");
       $(".legendCMobile").css("z-index","99");
     });
     $(".close").on('click', function(){
        window.onscroll = function() {}; //enable scrolling
        $(".zoomImgC").css({"display":"none"});
        $(".close").css({"display":"none"});
       $("body").css({"overflow":"auto"});
       $(".legendC").css("z-index","99");
       $(".legendCMobile").css("z-index","99");
     });
     /*start of code from club list*/
  var subClubDisplay = document.querySelector(".subClubDisplay");
  var scrollID = "";
  var mainArray = [];
  var steamArray = [];
  var steamOnlyOn = true;
  var numOfClubs = 0; 
  var numOfSTEAMClubs = 0;
  var clubListing = document.querySelector(".subClubDisplay");
  function updateClubListing() {
    mainArray = [];
    steamArray = [];
    numOfSTEAMClubs = 0;
    for (var index = 0; index < roomListArr.length; index++) {
      mainArray.push(roomListArr[index].teacher);
      //this creates a new element
      var listItem = document.createElement("LI");
      listItem.id = `item${index+1}`;
      listItem.classList.add("linkItem");
      subClubDisplay.appendChild(listItem);
      var listItemS = document.createElement("div");
      listItemS.classList.add("gridC");
      if (roomListArr[index].dept != "other") {
        switch (roomListArr[index].dept) {
          case "s":
            listItemS.style.borderLeft = "4px solid #8ac926";
            break;
          case "t":
            listItemS.style.borderLeft = "4px solid #1982c4";
            break;
          case "e":
            listItemS.style.borderLeft = "4px solid #6a4c93";
            break;
          case "a":
            listItemS.style.borderLeft = "4px solid #ffca3a";
            break;
          case "m":
            listItemS.style.borderLeft = "4px solid #ff595e";
            break;
        }
      }
      listItem.appendChild(listItemS); //this finishes the li with .gridC class div
      //now the .gridC class div has to be added on to
      var listItemSS1 = document.createElement("div");
      listItemSS1.style.paddingRight = "4px";
      var listItemSS2 = document.createElement("div");//has text for type of club
      listItemS.appendChild(listItemSS1);listItemS.appendChild(listItemSS2);
      var listItemSS1A = document.createElement("a");//has text/link for name of club
      listItemSS1A.classList.add("linkItemA");
      //listItemSS1A.href = "";
      listItemSS1.appendChild(listItemSS1A);
      //now only the text has to be created for these elements
      var tempStrInsert = "";
      if (roomListArr[index].course) { tempStrInsert=roomListArr[index].course; }
      else if (roomListArr[index].courses) {
        for (var index4 = 0; index4 < roomListArr[index].courses.length; index4++) {
          tempStrInsert += roomListArr[index].courses[index4];
          if (index4 < (roomListArr[index].courses.length-1)) { tempStrInsert += ", "; }
        }
      }
      var listItemSS1ATxt = document.createTextNode(`${roomListArr[index].teacher} - ${tempStrInsert}`);
      listItemSS1A.appendChild(listItemSS1ATxt);
      var listItemSS2Txt;
      if (roomListArr[index].room) {
        listItemSS2Txt = document.createTextNode(`${roomListArr[index].room}`);
      }
      listItemSS2.appendChild(listItemSS2Txt);
    }
  }
  function updateClubInListing(index17) {
      //this creates a new element
      var listItem = document.createElement("LI");
      listItem.id = `item${index17+1}`;
      listItem.classList.add("linkItem");
      subClubDisplay.appendChild(listItem);
      var listItemS = document.createElement("div");
      listItemS.classList.add("gridC");
      if (roomListArr[index17].dept != "other") {
        switch (roomListArr[index17].dept) {
          case "s":
            listItemS.style.borderLeft = "4px solid #8ac926";
            break;
          case "t":
            listItemS.style.borderLeft = "4px solid #1982c4";
            break;
          case "e":
            listItemS.style.borderLeft = "4px solid #6a4c93";
            break;
          case "a":
            listItemS.style.borderLeft = "4px solid #ffca3a";
            break;
          case "m":
            listItemS.style.borderLeft = "4px solid #ff595e";
            break;
        }
      }
      if (checked) { listItemS.style.borderLeft = "4px solid #8B8B8B"; }
      listItem.appendChild(listItemS); //this finishes the li with .gridC class div
      //now the .gridC class div has to be added on to
      var listItemSS1 = document.createElement("div");
      listItemSS1.style.paddingRight = "4px";
      var listItemSS2 = document.createElement("div");//has text for type of club
      listItemS.appendChild(listItemSS1);listItemS.appendChild(listItemSS2);
      var listItemSS1A = document.createElement("a");//has text/link for name of club
      listItemSS1A.classList.add("linkItemA");
      //listItemSS1A.href = "";
      listItemSS1.appendChild(listItemSS1A);
      //now only the text has to be created for these elements
      var tempStrInsert = "";
      if (roomListArr[index17].course) { tempStrInsert=roomListArr[index17].course; }
      else if (roomListArr[index17].courses) {
        for (var index4 = 0; index4 < roomListArr[index17].courses.length; index4++) {
          tempStrInsert += roomListArr[index17].courses[index4];
          if (index4 < (roomListArr[index17].courses.length-1)) { tempStrInsert += ", "; }
        }
      }
      var listItemSS1ATxt = document.createTextNode(`${roomListArr[index17].teacher} - ${tempStrInsert}`);
      listItemSS1A.appendChild(listItemSS1ATxt);
      var listItemSS2Txt;
      if (roomListArr[index17].room) {
        listItemSS2Txt = document.createTextNode(`${roomListArr[index17].room}`);
      }
      listItemSS2.appendChild(listItemSS2Txt);
  }
  function clearClubListing(clubListing) {
    while(clubListing.firstChild) {
      clubListing.removeChild(clubListing.firstChild);
    }
  }
  function displayClub(clubID) {
    //this sets the user's current page scroll position
    scrollID = clubID;
    //this switches the view from the list to more information
    $("#club-select").css("display","none");
    $("#club-body").css("display","block");
    //this automatically scrolls to the bottom of the page
    var clubBody = document.querySelector("#club-body");
    //this gets the index of the current selected object based on its id
    var index = parseInt(clubID.replace( /^\D+/g, ''))-1;
    var currentObj = roomListArr[index];
    if (currentObj.banner_image) {$("#club-notice").css("background-image", `url("${currentObj.banner_image}")`)}
    else if (checked) { $("#club-notice").css("background-image", `url("/static/iconblack-01.svg")`) }
    else { $("#club-notice").css("background-image", `url("/static/STEAM-icon-04.svg")`) }
    var tempStrInsert = "";
      if (currentObj.course) { tempStrInsert=currentObj.course; }
      else if (currentObj.courses) {
        for (var index4 = 0; index4 < currentObj.courses.length; index4++) {
          tempStrInsert += currentObj.courses[index4];
          if (index4 < (currentObj.courses.length-1)) { tempStrInsert += ", "; }
        }
      }
    $("#course-teacher").text(tempStrInsert);
    $("#course-name").text(currentObj.teacher);
    $("#course-room").text(currentObj.room);
      $("#course-clubsC").css("display", "none");
      if (currentObj.clubs[0] || currentObj.organizations[0]) {
        var tempSList = "";
        $("#course-clubsC").css("display", "block");
        for (var index4 = 0; index4 < currentObj.clubs.length; index4++) {
          tempSList += currentObj.clubs[index4];
          if (index4 < (currentObj.clubs.length-1)) { tempSList += ", "; }
        }
        for (var index4 = 0; index4 < currentObj.organizations.length; index4++) {
          if (index4 == 0 && tempSList !="") { tempSList += ", "; }
          tempSList += currentObj.organizations[index4];
          if (index4 < (currentObj.organizations.length-1)) { tempSList += ", "; }
        }
        $("#course-clubs").text(tempSList);
      }
  }
  $(".subClubDisplay").on('click', '.linkItem', function() {
    var thisClubID = $(this).attr("id");
    $(".mainContent").css("display", "none");
    displayClub(thisClubID);
    //this is used to fix the footer positioning
    var vw = Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0);
    var vh = Math.max(document.documentElement.clientHeight || 0, window.innerHeight || 0);
    var elementOffset = $('.footerC').offset().top;
    var distance = (elementOffset)+$('.footerC').outerHeight();
    if ((vh-distance)>=0) { $('.footerC').css("position", "absolute");$('.footerC').css("bottom", "0px"); } 
    else { $('.footerC').css("position", "relative"); }
  });
  $("#returnToList").on('click', function() {
    $(".mainContent").css("display", "block");
    $("#club-select").css("display","block");
    $("#club-body").css("display","none");
    $('.footerC').css("position", "relative");
    var scrollIDElem = document.getElementById(`${scrollID}`);
    //window.scrollTo(0, scrollIDElem.offsetTop);
  });
/*end of code from club list*/
/*start of JavaScript for the search bar*/
var array = [];
var maxResults = 1000000000000; //This is the maximum number of results that will pop up in the keyword search. Set to any valid number.
var obj = {};
var tempString = "";
var selectedDept = ""; //this is to help open the correct info for searching
var selectedCourse = "";
var stopOffset2 = false;
var clubListing = document.querySelector(".subClubDisplay");

function stylePS(psElement) {
psElement.style.marginBottom = "0px";
}
function hoverStyleP(pElement) {
//This is used to change the color of search results background when hovered over
pElement.style.backgroundColor = "#0248b1";
}
function styleP(pElement) {//This is used to style each of the search results, change for better results
pElement.style.width = "200px";
pElement.style.height = "auto";
pElement.style.color = "white";
pElement.style.backgroundColor = "#3585fd";
pElement.style.fontSize = "15px";
pElement.style.padding = "0.5vmin";
pElement.style.margin = "0vmin";
//pElement.style.textAlign = "center";
}
function styleA(aElement) {//This is used to style the anchor tags, change for better results
aElement.style.color="white";
aElement.style.textDecoration= "none";
aElement.style.cursor="pointer";
}
function appendDiv(temp, txtOptDiv) {
if (stopOffset2) { $("#outputC").css("bottom",`-${$("#outputC").outerHeight()+25}px`); }
else { $("#outputC").css("bottom",`-${$("#outputC").outerHeight() + 50}px`); }
selectedCourse = temp;
var pElement = document.createElement("div");
var pTxt = document.createElement("P"); //this creates a new <p> element
pTxt.classList.add("searchResult");
var aElement = document.createElement("A"); //this creates a new <a> element
aElement.style.textDecoration = "none";
var txt = document.createTextNode(temp); //this puts the search result into a text field
//var link = "#";
var counter = 0;
stylePS(pTxt);
styleA(aElement);
aElement.appendChild(pElement);
pElement.appendChild(pTxt);
pTxt.appendChild(txt); //this places the text inside of the new element
pElement.onmouseover=function() {hoverStyleP(pElement)};
pElement.onmouseout=function() {styleP(pElement)};
styleP(pElement);
txtOptDiv.appendChild(aElement); //this appends the new element to the content div
//aElement.href=link;
}
function clearDiv(txtOptDiv) {
while(txtOptDiv.firstChild) {
txtOptDiv.removeChild(txtOptDiv.firstChild);
}
}
function searchResults() {
array = mainArray;
$("#outputC").css("bottom",`-${$("#outputC").outerHeight() + 50}px`);
obj = {};
var highestCount = -1;
stopOffset2 = false;
var cont = true;
var cont2 = true;
var cont3 = true;
var txtIpt = document.getElementById("search").value;
var txtIptL = (txtIpt.toLowerCase()).replace(/[\/\\]/g,'');
var txtOptDiv = document.getElementById("outputC");
if (txtIptL == "" || txtIptL == " ") {
clearClubListing(clubListing);
updateClubListing();
$('.footerC').css("position", "relative");
}
else {
$('.footerC').css("position", "relative");
//this is used to fix the footer positioning
var vw = Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0);
var vh = Math.max(document.documentElement.clientHeight || 0, window.innerHeight || 0);
var elementOffset = $('.footerC').offset().top;
var distance = (elementOffset)+$('.footerC').outerHeight();
if ((vh-distance)>=0) { $('.footerC').css("position", "absolute");$('.footerC').css("bottom", "0px"); } 
else { $('.footerC').css("position", "relative"); }
clearClubListing(clubListing);
}
clearDiv(txtOptDiv); //this is used to make sure that the search results are cleared after each use
if (!txtIptL[1]) {
$("#outputC").css("bottom",`-${$("#outputC").outerHeight()+25}px`);
stopOffset2 = true;
}
for (var index=0; index<array.length; index++) {
temp = array[index];
tempL = (array[index].toLowerCase()).replace(/[\/\\]/g,' ');
if ((tempL == txtIptL) || (txtIptL == "acdc electronics" && tempL == "ac dc electronics")) { //eliminate all other results on a perfect match
//$("#outputC").css("bottom",`-${$("#outputC").outerHeight()+25}px`);
stopOffset2 = true;
cont2 = false;
//appendDiv(temp, txtOptDiv); //temp here is used to assign a link to the correct search result
var foundIndex;
for (var index17 = 0; index17 < mainArray.length; index17++) {
if (mainArray[index17] == temp) {
  foundIndex = index17;
  break;
}
}
updateClubInListing(foundIndex);
break;
}
}
if (cont2) { //if a perfect match was not already found
for (var index=0; index<array.length; index++) { //this searches the entire list
cont=true;
var temp = array[index];
var tempL = (temp.toLowerCase()).replace(/[\/\\]/g,' ');
var count = 0;
for (var i=0; i<tempL.length; i++) { //this searches each character inside of string for each element of the array
for(var i2=0; i2<txtIptL.length; i2++) { //this searches each character inside of the input string separately
if (tempL[i] == txtIptL[i2]) {
  cont=false;
  count++;
  break;
}
}
}
if (count > highestCount) {
highestCount = count; //this updates the highest counted number (most accurate search result)
}
//this checks to see if the first word of the career is similar to the first part of the first word that the user types in the search
var checkerIndx = tempL.indexOf(txtIptL);
if (checkerIndx != -1) {
//success! in this case, it found the user input lowercase string to be part of the lowercase array results
highestCount+=40; //a really high value so that it takes priority
count = highestCount;
}
obj[temp] = count; //this updates the count for each item
}
var objectLength = Object.keys("obj").length; //this returns the object's length, not needed right now
//this is used to make sure that the search results appear in the highest order first
var resultCounter = 0;
for (var index=highestCount; index>0; index--) {
for (var index2=0; index2<array.length; index2++) {
var temp3 = array[index2];
var temp4 = obj[temp3];
if (resultCounter == maxResults) {
cont3=false;
break;
}
if (temp4 == index) {
resultCounter++;
//appendDiv(temp3, txtOptDiv); //this takes care of updating the search results
var foundIndex;
for (var index17 = 0; index17 < mainArray.length; index17++) {
if (mainArray[index17] == temp3) {
  foundIndex = index17;
  break;
}
}
updateClubInListing(foundIndex);
}
}
if (!cont3) { //same thing as cont3 == false
break;
}
}
}
if (txtIptL == "" || txtIptL == " ") {
clearClubListing(clubListing);
updateClubListing();
$('.footerC').css("position", "relative");
}
else {
$('.footerC').css("position", "relative");
//this is used to fix the footer positioning
var vw = Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0);
var vh = Math.max(document.documentElement.clientHeight || 0, window.innerHeight || 0);
var elementOffset = $('.footerC').offset().top;
var distance = (elementOffset)+$('.footerC').outerHeight();
if ((vh-distance)>=0) { $('.footerC').css("position", "absolute");$('.footerC').css("bottom", "0px"); } 
else { $('.footerC').css("position", "relative"); }
}
}
//this pulls up the course information and scrolls to the section where its dept's courses list is
$("#outputC").on('click', ".searchResult", function() {
var searchResTxt = $(this).text();
var elem4ID = $(`.subClubDisplay li:contains(${searchResTxt})`).attr("id");
var curElement = document.getElementById(`${elem4ID}`);
//this scrolls to the actual search result
window.scrollTo(0, curElement.offsetTop);
//this takes care of opening the information of the club or organization automatically
var thisClubID = elem4ID
displayClub(thisClubID);
});
$(".search-icon").on('click', function(){}, function() {
var txtOptDiv = document.getElementById("outputC");
clearDiv(txtOptDiv);
});
/*End of JavaScript for the search bar*/
