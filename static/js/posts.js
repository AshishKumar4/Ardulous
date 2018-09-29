function makeCommentPost(pid)
{
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () 
    {
        if (this.readyState == 4 && this.status == 200) 
        {
            //feedpos += fetchCount;
            //d.innerHTML = createMultiPostCards(this.responseText);
        }
    };
    xhttp.open("POST", "/handlers/postcomment", true);
    xhttp.send(JSON.stringify({postid: pid}));
}

function makeLikePost(pid)
{
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () 
    {
        if (this.readyState == 4 && this.status == 200) 
        {
            //feedpos += fetchCount;
            //d.innerHTML = createMultiPostCards(this.responseText);
            var d = document.getElementById(pid).getElementsByClassName("post-like-button")[0];
            d.childNodes[1].classList = "glyphicon glyphicon-heart"; 	
        }
    };
    xhttp.open("POST", "/handlers/postlike", true);
    xhttp.send(JSON.stringify({postid: pid}));
}

$('.post-like-button').click(function(){
    $(this).css('color','red');
  });

function makeSharePost(pid)
{
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () 
    {
        if (this.readyState == 4 && this.status == 200) 
        {
            //feedpos += fetchCount;
            //d.innerHTML = createMultiPostCards(this.responseText);
        }
    };
    xhttp.open("POST", "/handlers/postshare", true);
    xhttp.send(JSON.stringify({postid: pid}));
}

function createPostCard(data)
{
    var s = "";
    
    s = '<div class="container posts" id="'+data['post-id']+'"> <div class="post-header container"> <div class="post-author-card"> <div class="post-author"> <div class="post-author-pic"> <img class="post-author-pic-img" src="'+data['author-pic']+'" /> </div> <div class="post-author-name"> '+data['author-name']+' </div> </div> </div> <div class="post-datetime"> '+data['time']+' </div> </div> <div class="post-body container"> <div class="post-text"> '+data['text']+' </div> </div> <div class="post-interactions container"> <div class="post-like-button" onclick="makeLikePost(\''+data['post-id']+'\')"> <div class="glyphicon glyphicon-heart-empty"></div> '+data['stats-likes']+' </div> <div class="post-comment-button" onclick="makeCommentPost(\''+data['post-id']+'\')"> <div class="glyphicon glyphicon-comment"></div> '+data['stats-comments']+' </div> <div class="post-share-button" onclick="makeSharePost(\''+data['post-id']+'\')"> <div class="glyphicon glyphicon-share"></div> '+data['stats-shares']+' </div> </div> <div class="post-comments container"> </div> </div>';
    
    return s.replace(/undefined/g, "");
}

function createMultiPostCards(data)
{
    var dd = JSON.parse(data);
    var s = "";
    for(var i = 0; i < dd.length; i++)
    {
        s += createPostCard(dd[i]);
    }
    return s;
}

var feedpos = 0;

function loadPostFeed(cc, offset) 
{
    var d = document.getElementById("post-area");
    var fetchCount = cc;
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () 
    {
        if (this.readyState == 4 && this.status == 200) 
        {
            feedpos += fetchCount;
            d.innerHTML += createMultiPostCards(this.responseText);
        }
    };
    xhttp.open("POST", "/handlers/feedfetch", true);
    xhttp.send(JSON.stringify({count:fetchCount, feedpos:feedpos-offset}));
}

function loadPostsAll(uid, cc, offset) 
{
    var d = document.getElementById("post-area");
    var fetchCount = cc;
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () 
    {
        if (this.readyState == 4 && this.status == 200) 
        {
            feedpos += fetchCount;
            d.innerHTML += createMultiPostCards(this.responseText);
        }
    };
    xhttp.open("POST", "/handlers/originalsfetch", true);
    xhttp.send(JSON.stringify({user:uid, count:fetchCount, feedpos:feedpos-offset}));
}

function loadLatestPosts(cc)
{   
    var d = document.getElementById("post-area");
    var fetchCount = cc;
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () 
    {
        if (this.readyState == 4 && this.status == 200) 
        {
            feedpos += fetchCount;
            d.innerHTML = createMultiPostCards(this.responseText) + d.innerHTML;
        }
    };
    xhttp.open("POST", "/handlers/feedfetch", true);
    xhttp.send(JSON.stringify({count:fetchCount, feedpos:0}));
}

function uploadContent()
{
    var d = document.getElementById("uploadcontent");
    d.click();
}

function newPost()
{
    var d = document.getElementById("post-create-text");
    var ff = document.getElementById("uploadcontent");
    postdata = {time : Date(), text : d.textContent, file : ""};
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () 
    {
        if (this.readyState == 4 && this.status == 200) 
        {
            document.getElementById("status").innerHTML = this.responseText;
            loadLatestPosts(1);
        }
    };
    xhttp.open("POST", "/handlers/newpost", true);
    xhttp.send(JSON.stringify(postdata));
}


