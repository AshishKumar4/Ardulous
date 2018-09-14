


function loadPostsAll(uid) 
{
    var d = document.getElementById("post-area");

}

function createPostCard(data)
{
    var s = "";
    
    s = '<div class="container posts"> <div class="post-header container"> <div class="post-author-card"> <div class="post-author"> <div class="post-author-pic"><img class="post-author-pic-img" src="'+data['author-pic']+'" /></div> <div class="post-author-name"> '+data['author-name']+' </div> </div> </div> <div class="post-datetime"> '+data['time']+' </div> </div> <div class="post-body container"> <div class="post-text"> '+data['text']+' </div> </div> <div class="post-interactions container"> <div class="post-like-button"> <div class="glyphicon glyphicon-heart-empty"></div> '+data['stats-likes']+' </div> <div class="post-comment-button"> <div class="glyphicon glyphicon-comment"></div> '+data['stats-comments']+' </div> <div class="post-share-button"> <div class="glyphicon glyphicon-share"></div> '+data['stats-shares']+' </div> </div> <div class="post-comments container"> </div> </div> ';
    
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

function loadPostFeed() 
{
    var d = document.getElementById("post-area");
    var fetchCount = 5;
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () 
    {
        if (this.readyState == 4 && this.status == 200) 
        {
            d.innerHTML = createMultiPostCards(this.responseText);
        }
    };
    xhttp.open("POST", "/handlers/feedfetch", true);
    xhttp.send(JSON.stringify({"count":fetchCount}));
}

function newPost()
{
    var d = document.getElementById("post-create-text");
    postdata = {time : Date(), text : d.textContent, file : ""};
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () 
    {
        if (this.readyState == 4 && this.status == 200) 
        {
            document.getElementById("status").innerHTML = this.responseText;
        }
    };
    xhttp.open("POST", "/handlers/newpost", true);
    xhttp.send(JSON.stringify(postdata));
}